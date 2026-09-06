import shutil
from termly.commands import get_available_commands
from termly.documentation import get_help
from termly.knowledge_model import CommandKnowledge, CommandInventory

def discover_command(command):
    available_commands = get_available_commands()

    if command not in available_commands:
        return None

    help_text = get_help(command)

    return CommandKnowledge(
        command=command,
        phrases=[],
        keywords=[],
        description="",
        example=command,
        help_text=help_text,
        source="help",
    )

def discover_commands():
    available_commands = get_available_commands()
    results = []

    for command in available_commands:
        path = shutil.which(command)
        if path is None:
            continue

        results.append(
            CommandInventory(
                command=command,
                path=path,
            )
        )

    return results

def discover_command_inventory():
    available_commands = get_available_commands()

    results = []

    for command in available_commands:
        path = shutil.which(command)

        if path is None:
            continue

        results.append(
            CommandInventory(
                command=command,
                path=path,
            )
        )

    return results
