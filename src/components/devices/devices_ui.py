import flet as ft
from flet.core.colors import Colors

from src.components.load_commands.load_commands_core import update_selected_device

from .devices_core import get_devices



def create_devices_section(page, device_var, terminal_output):
    header_row = ft.Row(
        spacing=10,
        controls=[],
        alignment=ft.MainAxisAlignment.START,
    )

    device_label = ft.Text(
        value="Select a device",
        size=16,
        color=ft.Colors.WHITE,
        text_align=ft.TextAlign.CENTER,
        col={"sm": 12}
    )

    update_icon = ft.IconButton(
        icon=ft.icons.REFRESH,
        on_click=lambda e: update_devices(e, page),
        bgcolor=Colors.BLUE_600,
        icon_color=Colors.WHITE

    )

    header_row.controls.append(device_label)
    header_row.controls.append(update_icon)

    devices_section = ft.Row(
        spacing=10,
        controls=[],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    devices = get_devices()
    device_buttons = []

    def create_device_buttons(devices):
        nonlocal device_buttons
        device_buttons.clear()
        for device in devices:
            button = ft.ElevatedButton(
                text=device,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.GREY_800,
                    color=ft.Colors.WHITE,
                    shape=ft.RoundedRectangleBorder(radius=5),
                    padding=ft.padding.symmetric(vertical=10, horizontal=20),
                ),
                on_click=lambda e, d=device: update_selected_device(page,device_var,device_buttons, terminal_output, d),
                col={"sm": 6, "md": 4, "lg": 3}
            )
            device_buttons.append(button)
            devices_section.controls.append(button)

    create_device_buttons(devices)


    def update_devices(e, page):
        current_devices = get_devices()
        if set(current_devices) != set(devices):
            devices.clear()
            devices.extend(current_devices)

            devices_section.controls.clear()
            create_device_buttons(devices)
            page.update()

    return ft.Row(
        controls=[header_row, devices_section],
        expand=True
    )
