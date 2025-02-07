from src.components.terminal.terminal_section_core import execute_command
import flet as ft

def get_devices():
    command = "adb devices | grep -w 'device' | awk '{print $1}'"
    result = execute_command(command)
    devices = result.splitlines()
    return devices


def get_emulator_port(device_var: ft.Text, terminal_output: ft.Text) -> str:
    device_id = device_var.value
    
    if device_id.startswith("emulator-"):
        port = device_id.split("-")[-1]
        return port
    
    terminal_output.value += "Cannot retrieve port from a device that is not an emulator.\n"
    return ""
