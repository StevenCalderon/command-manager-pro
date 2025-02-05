import flet as ft
from flet.core.colors import Colors


def create_app_dropdown(config, app_var, terminal_output, page):
    app_dict = {app["name"]: app for app in config["applications"]}

    dropdown = ft.Dropdown(
        label="Select application",
        label_style=ft.TextStyle(
            color=Colors.WHITE,
            weight=ft.FontWeight.BOLD,
            size=14,
        ),
        options=list(map(lambda app: ft.dropdown.Option(app["name"]), config["applications"])),
        #width=200,
        bgcolor="#424242",
        color=Colors.WHITE,
        border_radius=5,
        focused_border_color=Colors.BLUE_800,
        filled=True,
        col={"sm": 12, "md": 6, "lg": 4}
    )

    def app_selected(e):
        selected_name = e.control.value
        if selected_name in app_dict:
            app_var.value = app_dict[selected_name]["package"]
            terminal_output.value += f"Selected application: {selected_name} ({app_dict[selected_name]['package']})\n"
        page.update()

    dropdown.on_change = app_selected
    return dropdown

def create_select_app(config, app_var, terminal_output, page):
    dropdown = create_app_dropdown(config, app_var, terminal_output, page)
    section = ft.ResponsiveRow(spacing=10, alignment=ft.MainAxisAlignment.CENTER, controls=[dropdown])

    return {"section": section, "app_dropdown": dropdown}
