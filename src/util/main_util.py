import os

import flet as ft
from components.devices.devices_ui import create_devices_section
from components.menu_bar.menu_bar_ui import create_menu_bar
from components.panels.panels_ui import create_panels
from components.select_app.select_app_ui import create_select_app
from components.terminal.terminal_section_ui import create_terminal
from components.load_commands.load_commands_core import load_last_config_path, load_config
from components.devices.devices_core import get_emulator_port

def initialize_ui(page: ft.Page, update_ui):
    terminal_output, bottom_terminal, real_terminal = create_terminal(page)

    last_config_path = load_last_config_path()
    config = None

    if last_config_path and os.path.exists(last_config_path):
        try:
            config = load_config(last_config_path)
            terminal_output.value += f"Configuration loaded: {last_config_path}\n"
        except Exception as e:
            terminal_output.value += f"Error loading configuration: {str(e)}\n"
            config = None

    if not config:
        config = {"applications": [], "panels": []}

    app_var = ft.Text(value="")
    device_var = ft.Text(value="")

    app_section = create_select_app(config, app_var, terminal_output, page)
    menubar = create_menu_bar(page, app_section["app_dropdown"], terminal_output, update_ui)

    devices_section = create_devices_section(page, device_var, terminal_output)
    
    def get_dynamic_variables():
        dynamic_variables = {
            "device": device_var.value,
            "app_package": app_var.value,
            **config.get("variables", {}),
        }
        port_emulator = get_emulator_port(device_var,terminal_output)
        if port_emulator.isdigit():  
            dynamic_variables["port_emulator"] = port_emulator
        
        return dynamic_variables
    
    panels_section = create_panels(config, get_dynamic_variables, terminal_output, page)


    return {
        "terminal_output": terminal_output,
        "bottom_terminal": bottom_terminal,
        "real_terminal": real_terminal,
        "config": config,
        "app_var": app_var,
        "devices_section": devices_section,
        "app_section": app_section,
        "menubar": menubar,
        "panels_section": panels_section
    }