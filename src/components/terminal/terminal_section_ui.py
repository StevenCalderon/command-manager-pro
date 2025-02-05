import flet as ft
import subprocess
import threading
import sys
import os

from flet.core.colors import Colors
from flet.core.icons import Icons


class RealTerminal:
    def __init__(self, output_callback):
        self.output_callback = output_callback
        self.process = None
        self.running = False
        self.history = []
        self.history_index = 0
        self.shell = self.detect_shell()

    def detect_shell(self):
        if sys.platform == "win32":
            return "cmd.exe"
        return "/bin/bash"

    def start(self):
        self.running = True
        self.process = subprocess.Popen(
            [self.shell],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            shell=True if sys.platform == "win32" else False,
        )
        self.read_output()

    def read_output(self):
        def read_stream(stream, callback):
            while self.running:
                output = stream.readline()
                if output:
                    callback(output)
                else:
                    break

        threading.Thread(target=read_stream, args=(self.process.stdout, self.output_callback), daemon=True).start()
        threading.Thread(target=read_stream, args=(self.process.stderr, self.output_callback), daemon=True).start()

    def send_command(self, command):
        if self.process and self.process.stdin:
            self.process.stdin.write(command + "\n")
            self.process.stdin.flush()
            self.history.append(command)
            self.history_index = len(self.history)

    def get_previous_command(self):
        if self.history_index > 0:
            self.history_index -= 1
            return self.history[self.history_index]
        return ""

    def get_next_command(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            return self.history[self.history_index]
        return ""

    def stop(self):
        self.running = False
        if self.process:
            self.process.terminate()


def create_terminal(page):
    terminal_output = ft.TextField(
        value="Welcome to Commands Manager Pro Terminal!\n",
        multiline=True,
        read_only=True,
        color=Colors.GREEN_ACCENT_400,
        text_size=13,
        expand=True,
    )

    terminal_output_container = ft.ListView(
        auto_scroll=True,
        expand=True,
    )
    terminal_output_container.controls.append(terminal_output)

    command_input = ft.TextField(
        hint_text="Type a command and press Enter...",
        hint_style=ft.TextStyle(color=Colors.BLACK),
        bgcolor="#cccccc",
        color=Colors.BLACK,
        border_color=Colors.GREY_700,
        border_radius=5,
        text_size=13,
        height=35,
        on_submit=lambda e: (
            send_command_to_terminal(e.control.value, terminal_output, real_terminal),
            setattr(e.control, "value", ""),
            e.control.update()
        ),
    )

    def send_command_to_terminal(command, output_field, terminal):
        if command.strip():
            terminal.send_command(command)
            output_field.value += f"$ {command}\n"
            output_field.update()

    def clear_terminal(output_field, page):
        output_field.value = ""
        page.update()

    real_terminal = RealTerminal(lambda output: update_terminal_output(terminal_output, output))
    real_terminal.start()

    def update_terminal_output(output_field, output):
        if output_field.page:
            output_field.value += output
            output_field.update()

    toolbar = ft.Row(
        controls=[
            ft.IconButton(
                icon=Icons.DELETE,
                icon_color=Colors.RED_500,
                tooltip="Clear Terminal",
                on_click=lambda _: clear_terminal(terminal_output, page),
                scale=0.85,
            ),
            ft.IconButton(
                icon=Icons.CONTENT_COPY,
                icon_color=Colors.BLUE_500,
                tooltip="Copy Output",
                on_click=lambda _: copy_terminal_output(terminal_output, page),
                scale=0.85,
            ),
            ft.IconButton(
                icon=Icons.CONTENT_PASTE,
                icon_color=Colors.GREEN_500,
                tooltip="Paste Command",
                on_click=lambda _: paste_to_terminal(command_input, page),
                scale=0.85,
            ),
        ],
        spacing=0,
        offset=ft.Offset(0, -0.05),
        alignment=ft.MainAxisAlignment.END,
    )

    def copy_terminal_output(output_field, page):
        page.set_clipboard(output_field.value)
        page.snack_bar = ft.SnackBar(content=ft.Text("Output copied to clipboard!"))
        page.snack_bar.open = True
        page.update()

    def paste_to_terminal(input_field, page):
        input_field.value = page.get_clipboard()
        input_field.update()

    bottom_terminal = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=toolbar,
                    padding=0,
                    height=35,
                ),
                ft.Container(
                    content=terminal_output_container,
                    border_radius=ft.border_radius.all(5),
                    border=ft.border.all(1, Colors.GREY_700),
                    bgcolor=Colors.BLACK,
                    height=135,
                    expand=True,
                    padding=0,
                ),
                ft.Container(
                    content=command_input,
                    padding=ft.padding.symmetric(5, 0),
                    margin=ft.margin.only(bottom=10),
                ),
            ],
            auto_scroll=True,
            spacing=0,
        ),
        bgcolor=Colors.GREY_800,
        padding=ft.padding.symmetric(0, 15),
        border=ft.border.all(1, Colors.GREY_600),
        border_radius=ft.border_radius.only(10, 10, 0, 0),
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=15,
            color=ft.colors.BLACK54,
            offset=ft.Offset(2, 2),
        ),
    )

    return terminal_output, bottom_terminal, real_terminal
