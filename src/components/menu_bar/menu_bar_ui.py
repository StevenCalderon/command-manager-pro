import flet as ft

from flet.core.colors import Colors
from components.load_commands.load_commands_core import update_config_from_file


def create_menu_bar(page: ft.Page, app_combo, terminal_output, update_ui):
    def _update_ui():
        page.controls.clear()
        update_ui(page)
        page.update()
    
    file_picker = ft.FilePicker(on_result=lambda e: update_config_from_file(e, app_combo, terminal_output, _update_ui))

    menubar = ft.MenuBar(
        expand=True,
        style=ft.MenuStyle(
            alignment=ft.alignment.top_left,
            bgcolor="#424242",
            mouse_cursor={
                ft.ControlState.HOVERED: ft.MouseCursor.WAIT,
                ft.ControlState.DEFAULT: ft.MouseCursor.ZOOM_OUT,
            },
            elevation=10,
            side=ft.BorderSide(1, Colors.GREY_600),
        ),
        controls=[
            ft.MenuItemButton(
                content=ft.Text("Load Commands", size=12, color="#FFFFFF"),
                leading=ft.Icon(ft.Icons.FOLDER_OPEN, size=16, color="#FFFFFF"),
                style=ft.ButtonStyle(
                    bgcolor={ft.ControlState.HOVERED: "#1565c0"},
                    shape=ft.RoundedRectangleBorder(radius=4),
                    elevation=2,
                    padding=ft.padding.symmetric(horizontal=8),
                ),
                on_click=lambda _: file_picker.pick_files(allow_multiple=False),
            ),
            # ft.MenuItemButton(
            #     content=ft.Text("Load Plugin", size=12, color="#FFFFFF"),
            #     leading=ft.Icon(ft.Icons.SETTINGS, size=16, color="#FFFFFF"),
            #     style=ft.ButtonStyle(
            #         bgcolor={ft.ControlState.HOVERED: "#1565c0"},
            #         shape=ft.RoundedRectangleBorder(radius=4),
            #         elevation=2,
            #         padding=ft.padding.symmetric(horizontal=8),
            #     ),
            #     on_click=lambda e: print("Load Plugin clicked"),
            # ),
            # ft.MenuItemButton(
            #     content=ft.Text("New Tab", size=12, color="#FFFFFF"),
            #     leading=ft.Icon(ft.Icons.TAB, size=16, color="#FFFFFF"),
            #     style=ft.ButtonStyle(
            #         bgcolor={ft.ControlState.HOVERED: "#1565c0"},
            #         shape=ft.RoundedRectangleBorder(radius=4),
            #         elevation=2,
            #         padding=ft.padding.symmetric(horizontal=8),
            #     ),
            #     on_click=lambda e: print("New Tab clicked"),
            # ),
            ft.MenuItemButton(
                content=ft.Text("Reload Config", size=12, color="#FFFFFF"),
                leading=ft.Icon(ft.Icons.REFRESH, size=16, color="#FFFFFF"),
                style=ft.ButtonStyle(
                    bgcolor={ft.ControlState.HOVERED: "#1565c0"},
                    shape=ft.RoundedRectangleBorder(radius=4),
                    elevation=2,
                    padding=ft.padding.symmetric(horizontal=8),
                ),
                on_click=lambda e: _update_ui(),
            ),
        ],
    )

    page.overlay.append(file_picker)
    return menubar
