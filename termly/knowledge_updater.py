from termly.discovery import discover_command, discover_command_inventory
from termly.knowledge_store import (save_command, get_command, get_inventory, save_inventory,)

def update_command(database, command):
    discovered = discover_command(command)

    if discovered is None:
        return None

    existing = get_command(database, command)

    if existing is None:
        knowledge = discovered
    else:
        knowledge = type(existing)(
            command=existing.command,
            phrases=existing.phrases,
            keywords=existing.keywords,
            description=existing.description,
            example=existing.example,
            help_text=discovered.help_text,
            source=existing.source,
        )

    save_command(database, knowledge)
    return knowledge

def update_discovered_commands(database):
    discovered = discover_command_inventory()

    changed = find_new_or_changed_commands(database, discovered)

    results = []

    for inventory in changed:
        knowledge = update_command(database, inventory.command)

        if knowledge is None:
            continue

        save_inventory(database, inventory)
        results.append(knowledge)

    return results

def update_commands(database, commands):
    results = []

    for command in commands:
        result = update_command(database, command)

        if result is not None:
            results.append(result)

    return results

def find_new_or_changed_commands(database, discovered):
    results = []

    for inventory in discovered:
        existing = get_inventory(database, inventory.command)

        if existing is None:
            results.append(inventory)
            continue

        if existing.path != inventory.path:
            results.append(inventory)

    return results
