import flet as ft
import functools
from components.terminal.terminal_section_core import run_command

def create_panels(config, get_dynamic_variables, terminal_output, page):
    panels_section = ft.ResponsiveRow(spacing=20, alignment=ft.MainAxisAlignment.START)

    for panel in config["panels"]:
        commands_grid = ft.GridView(
            runs_count=3,
            max_extent=150,
            spacing=10,
            run_spacing=10,
            child_aspect_ratio=1.5,
        )

        for command in panel["commands"]:
            button_color = command.get("color", "#1565C0")

            command_button = ft.Container(
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            command["name"],
                            text_align=ft.TextAlign.CENTER,
                            color=ft.colors.WHITE,
                            size=12,
                            weight=ft.FontWeight.BOLD,
                        ),
                    ],
                ),
                on_click=lambda e, cmd=command["command"]: run_command(
                    page, get_dynamic_variables, terminal_output, cmd
                ),
                bgcolor=button_color,
                border_radius=10,
                padding=10,
                tooltip=command["command"],
                animate=ft.animation.Animation(50, "easeInOut"),
                on_hover=lambda e, base_color=button_color: on_hover(e, base_color),  # Maneja el hover
            )
            commands_grid.controls.append(command_button)

        # Crear el contenedor del panel
        panel_container = ft.Container(
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Text(panel["name"], size=18, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD),
                    commands_grid,
                ],
            ),
            padding=20,
            bgcolor=ft.colors.GREY_800,
            border_radius=10,
            border=ft.border.all(2, ft.colors.GREY_700),
            col={"sm": 12, "md": 6, "lg": 4},
        )
        panels_section.controls.append(panel_container)

    return panels_section

def on_hover(e, base_color):
    if e.data == "true":
        e.control.bgcolor = lighten_color(base_color, 0.2)
        e.control.scale = 1.1
    else:
        e.control.bgcolor = base_color
        e.control.scale = 1.0
    e.control.update()

def lighten_color(hex_color, factor=0.2):
    hex_color = hex_color.lstrip("#")
    r, g, b = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
    r = min(255, int(r + (255 - r) * factor))
    g = min(255, int(g + (255 - g) * factor))
    b = min(255, int(b + (255 - b) * factor))
    return f"#{r:02X}{g:02X}{b:02X}"
