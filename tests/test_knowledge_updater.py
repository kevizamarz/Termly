import pytest
from termly.knowledge_store import (initialize_database, get_command, save_command, seed_knowledge,)
from termly.knowledge_updater import (update_command, update_discovered_commands, find_new_or_changed_commands,)
from termly.knowledge_model import CommandKnowledge, CommandInventory
from termly.knowledge import KNOWLEDGE

def test_update_command(tmp_path):
    database = tmp_path / "termly.db"

    initialize_database(database)
    seed_knowledge(database, KNOWLEDGE)

    update_command(database, "ls")

    result = get_command(database, "ls")

    assert result is not None
    assert result.command == "ls"
    assert result.help_text is not None
    assert result.source == "builtin"


def test_update_command_preserves_curated_knowledge(tmp_path):
    database = tmp_path / "termly.db"

    initialize_database(database)
    seed_knowledge(database, KNOWLEDGE)

    original = get_command(database, "ls")
    assert original is not None

    update_command(database, "ls")

    result = get_command(database, "ls")

    assert result is not None
    assert result.phrases == original.phrases
    assert result.keywords == original.keywords
    assert result.description == original.description
    assert result.example == original.example
    assert result.help_text is not None


def test_update_unknown_command(tmp_path):
    database = tmp_path / "termly.db"

    initialize_database(database)

    result = update_command(
        database,
        "this_command_does_not_exist",
    )

    assert result is None
    assert get_command(database, "this_command_does_not_exist") is None

def test_update_commands(tmp_path, monkeypatch):
    database = tmp_path / "termly.db"

    initialize_database(database)

    def fake_update_command(database, command):
        knowledge = CommandKnowledge(
            command=command,
            phrases=[],
            keywords=[],
            description="",
            example=command,
            help_text=f"Help for {command}",
            source="help",
        )
        save_command(database, knowledge)
        return knowledge

    monkeypatch.setattr(
        "termly.knowledge_updater.update_command",
        fake_update_command,
    )

    from termly.knowledge_updater import update_commands

    results = update_commands(
        database,
        ["ls", "grep"],
    )

    assert len(results) == 2
    assert results[0].command == "ls"
    assert results[1].command == "grep"

    assert get_command(database, "ls") is not None
    assert get_command(database, "grep") is not None


def test_update_discovered_commands(tmp_path, monkeypatch):
    database = tmp_path / "termly.db"

    initialize_database(database)

    discovered = [
        CommandInventory(
            command="ls",
            path="/usr/bin/ls",
        ),
        CommandInventory(
            command="grep",
            path="/usr/bin/grep",
        ),
    ]

    monkeypatch.setattr(
        "termly.knowledge_updater.discover_command_inventory",
        lambda: discovered,
    )

    def fake_update_command(database, command):
        knowledge = CommandKnowledge(
            command=command,
            phrases=[],
            keywords=[],
            description="",
            example=command,
            help_text=f"Help for {command}",
            source="help",
        )
        save_command(database, knowledge)
        return knowledge

    monkeypatch.setattr(
        "termly.knowledge_updater.update_command",
        fake_update_command,
    )

    results = update_discovered_commands(database)

    assert len(results) == 2
    assert results[0].command == "ls"
    assert results[1].command == "grep"

    assert get_command(database, "ls") is not None
    assert get_command(database, "grep") is not None


def test_find_new_or_changed_commands(tmp_path):
    database = tmp_path / "test.db"

    from termly.knowledge_store import initialize_database, save_inventory

    initialize_database(database)

    save_inventory(
        database,
        CommandInventory(
            command="ls",
            path="/usr/bin/ls",
        ),
    )

    discovered = [
        CommandInventory(
            command="ls",
            path="/usr/bin/ls",
        ),
        CommandInventory(
            command="grep",
            path="/usr/bin/grep",
        ),
    ]

    result = find_new_or_changed_commands(database, discovered)

    assert result == [
        CommandInventory(
            command="grep",
            path="/usr/bin/grep",
        )
    ]


def test_incremental_update(tmp_path, monkeypatch):
    database = tmp_path / "termly.db"

    initialize_database(database)

    discovered = [
        CommandInventory(
            command="ls",
            path="/usr/bin/ls",
        ),
    ]

    monkeypatch.setattr(
        "termly.knowledge_updater.discover_command_inventory",
        lambda: discovered,
    )

    first_run = update_discovered_commands(database)

    assert len(first_run) == 1
    assert get_command(database, "ls") is not None

    second_run = update_discovered_commands(database)

    assert second_run == []

def test_update_new_command_extracts_knowledge(tmp_path, monkeypatch):
    database = tmp_path / "termly.db"
    initialize_database(database)

    help_text = """Usage: chmod [OPTION]... MODE FILE...
Change the mode of each FILE to MODE.
"""

    def fake_discover_command(command):
        return CommandKnowledge(
            command=command,
            phrases=[],
            keywords=[],
            description="",
            example=command,
            help_text=help_text,
            source="help",
        )

    monkeypatch.setattr(
        "termly.knowledge_updater.discover_command",
        fake_discover_command,
    )

    update_command(database, "chmod")

    result = get_command(database, "chmod")

    assert result is not None
    assert result.description == "Change the mode of each FILE to MODE."
    assert "change" in result.keywords
    assert "mode" in result.keywords
    assert result.phrases == ["change the mode of each file to mode"]
    assert result.help_text == help_text
    assert result.source == "help"
