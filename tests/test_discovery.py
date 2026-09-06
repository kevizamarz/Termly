from termly.discovery import (discover_command, discover_commands, discover_command_inventory,)
from termly.knowledge_model import CommandInventory

def test_discover_command():
    result = discover_command("ls")

    assert result is not None
    assert result.command == "ls"
    assert result.help_text is not None

def test_discover_unknown_command():
    result = discover_command("this_command_does_not_exist")

    assert result is None

def test_discover_commands(monkeypatch):
    monkeypatch.setattr(
        "termly.discovery.get_available_commands",
        lambda: {"ls", "grep"},
    )

    monkeypatch.setattr(
        "termly.discovery.shutil.which",
        lambda command: {
            "ls": "/usr/bin/ls",
            "grep": "/usr/bin/grep",
        }[command],
    )

    results = discover_commands()

    assert len(results) == 2
    assert all(isinstance(result, CommandInventory) for result in results)
    assert {result.command for result in results} == {"ls", "grep"}
    assert {result.path for result in results} == {
        "/usr/bin/ls",
        "/usr/bin/grep",
    }

def test_discover_command_inventory(monkeypatch):
    monkeypatch.setattr(
        "termly.discovery.get_available_commands",
        lambda: {"ls", "grep"},
    )

    monkeypatch.setattr(
        "termly.discovery.shutil.which",
        lambda command: {
            "ls": "/usr/bin/ls",
            "grep": "/usr/bin/grep",
        }[command],
    )

    results = discover_command_inventory()

    assert len(results) == 2
    assert {result.command for result in results} == {"ls", "grep"}
    assert {result.path for result in results} == {
        "/usr/bin/ls",
        "/usr/bin/grep",
    }
