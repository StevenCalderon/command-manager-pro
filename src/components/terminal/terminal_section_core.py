import subprocess

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return f"Error: {str(e)}"


def replace_text_with_values(text, variables):
    for key, value in variables.items():
        text = text.replace(f"{{{{{key}}}}}", str(value))
    return text

def run_command(page, get_dynamic_variables, terminal_output, command):
    dynamic_variables = get_dynamic_variables()
    new_command = replace_text_with_values(command, dynamic_variables)
    result = execute_command(new_command)
    terminal_output.value += f"$ {new_command}\n{result}\n\n"
    terminal_output.update()
    page.update()