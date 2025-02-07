import flet as ft
from flet.core.colors import Colors

from src.util.main_util import initialize_ui

ui = None
def main(page: ft.Page):
    global ui

    page.title = "Commands Manager Pro"
    page.bgcolor = Colors.GREY_900
    ui = initialize_ui(page, main)
    
    main_container = ft.Column(
        controls=[
            ui["devices_section"],
            ui["app_section"]["section"],
            ui["panels_section"],
        ],
        spacing=20,
        expand=True,
    )

    page.padding = 0
    page.add(ft.Row([ui["menubar"]]))
    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=main_container,
                        expand=True,
                        padding=10
                    ),
                ],
                expand=True,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=ft.padding.symmetric(0, 10),
            expand=True,
        ),
    )

    page.add(
        ft.Container(
            content=ui["bottom_terminal"],
            padding=0,
            margin=0,
        ),
    )

    page.spacing = 0
    page.border = 0
    page.on_close = lambda: ui["real_terminal"].stop()

    page.update()

if __name__ == "__main__":
    ft.app(target=main)
