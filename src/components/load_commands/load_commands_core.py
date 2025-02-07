import json
import os

import flet as ft

CONFIG_PATH_FILE = "config_path.json"

def save_config_path(filepath):
    with open(CONFIG_PATH_FILE, "w") as f:
        json.dump({"path": filepath}, f)

def load_last_config_path():
    if os.path.exists(CONFIG_PATH_FILE):
        with open(CONFIG_PATH_FILE, "r") as f:
            data = json.load(f)
            return data.get("path")
    return None

def load_config(filepath):
    with open(filepath, "r") as f:
        config = json.load(f)
    return config

def update_selected_device(page, device_var, device_buttons, terminal_output, device):
    device_var.value = device
    for button in device_buttons:
        if button.text == device:
            button.style = ft.ButtonStyle(bgcolor=ft.Colors.BLUE_800, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=5), padding=ft.padding.symmetric(vertical=10, horizontal=20))
        else:
            button.style = ft.ButtonStyle(bgcolor=ft.Colors.GREY_800, color=ft.Colors.WHITE, shape=ft.RoundedRectangleBorder(radius=5), padding=ft.padding.symmetric(vertical=10, horizontal=20),)
    terminal_output.value += f"Device selected: {device}\n"
    terminal_output.update()
    page.update()

def update_config_from_file(e: ft.FilePickerResultEvent, app_combo, terminal_output, update_ui ):
    if e.files:
        selected_path = e.files[0].path
        save_config_path(selected_path)
        try:
            new_config = load_config(selected_path)
            app_combo.options = [ft.dropdown.Option(app["name"]) for app in new_config["applications"]]
            terminal_output.value += f"Updated configuration from JSON: {selected_path}\n"
        except Exception as err:
            terminal_output.value += f"Error loading configuration: {str(err)}\n"
        update_ui()