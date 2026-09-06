import sqlite3
from termly.knowledge_model import CommandKnowledge, CommandInventory
from termly.knowledge_store import ( initialize_database, save_command, get_command, get_commands, save_inventory, get_inventory,)


def test_initialize_database(tmp_path):
    database = tmp_path / "termly.db"

    initialize_database(database)

    import sqlite3

    with sqlite3.connect(database) as connection:
        tables = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            """
        ).fetchall()

    assert ("commands",) in tables

def test_save_and_get_command(tmp_path):
    database = tmp_path / "termly.db"

    initialize_database(database)

    knowledge = CommandKnowledge(
        command="ls",
        phrases=["list files"],
        keywords=["list", "files"],
        description="List files",
        example="ls",
        help_text="Usage: ls [OPTION]...",
        source="help",
    )

    save_command(database, knowledge)

    result = get_command(database, "ls")

    assert result is not None
    assert result.command == "ls"
    assert result.help_text == "Usage: ls [OPTION]..."
    assert result.source == "help"


def test_save_multiple_commands(tmp_path):
    database = tmp_path / "termly.db"

    initialize_database(database)

    save_command(
        database,
        CommandKnowledge(
            command="ls",
            phrases=["list files"],
            keywords=["list", "files"],
            description="List files",
            example="ls",
            help_text="List information",
            source="help",
        ),
    )

    save_command(
        database,
        CommandKnowledge(
            command="grep",
            phrases=["search patterns"],
            keywords=["search", "patterns"],
            description="Search for patterns",
            example="grep pattern file",
            help_text="Search for patterns",
            source="help",
        ),
    )

    ls = get_command(database, "ls")
    grep = get_command(database, "grep")

    assert ls is not None
    assert ls.command == "ls"

    assert grep is not None
    assert grep.command == "grep"


def test_get_commands(tmp_path):
    database = tmp_path / "termly.db"

    initialize_database(database)
    clear_commands(database)

    save_command(
        database,
        CommandKnowledge(
            command="ls",
            phrases=["list files"],
            keywords=["list", "files"],
            description="List files",
            example="ls",
            help_text="List information",
            source="help",
        ),
    )

    save_command(
        database,
        CommandKnowledge(
            command="grep",
            phrases=["search patterns"],
            keywords=["search", "patterns"],
            description="Search for patterns",
            example="grep pattern file",
            help_text="Search for patterns",
            source="help",
        ),
    )

    commands = get_commands(database)

    assert len(commands) == 2
    assert {command.command for command in commands} == {"ls", "grep"}

def test_save_command_updates_existing_command(tmp_path):
    database = tmp_path / "termly.db"

    initialize_database(database)

    save_command(
        database,
        CommandKnowledge(
            command="ls",
            phrases=["list files"],
            keywords=["list", "files"],
            description="List files",
            example="ls",
            help_text="Old help",
            source="help",
        ),
    )

    save_command(
        database,
        CommandKnowledge(
            command="ls",
            phrases=["list files"],
            keywords=["list", "files"],
            description="List files",
            example="ls",
            help_text="New help",
            source="help",
        ),
    )

    result = get_command(database, "ls")

    assert result is not None
    assert result.help_text == "New help"


def test_save_command_does_not_create_duplicate(tmp_path):
    database = tmp_path / "termly.db"

    initialize_database(database)
    clear_commands(database)

    save_command(
        database,
        CommandKnowledge(
            command="ls",
            phrases=["list files"],
            keywords=["list", "files"],
            description="List files",
            example="ls",
            help_text="Old help",
            source="help",
        ),
    )

    save_command(
        database,
        CommandKnowledge(
            command="ls",
            phrases=["list files"],
            keywords=["list", "files"],
            description="List files",
            example="ls",
            help_text="New help",
            source="help",
        ),
    )

    commands = get_commands(database)

    assert len(commands) == 1
    assert commands[0].command == "ls"
    assert commands[0].help_text == "New help"

def test_save_and_get_inventory(tmp_path):
    database = tmp_path / "test.db"

    initialize_database(database)

    inventory = CommandInventory(
        command="ls",
        path="/usr/bin/ls",
    )

    save_inventory(database, inventory)

    with sqlite3.connect(database) as connection:
        row = connection.execute(
            """
            SELECT command, path
            FROM command_inventory
            WHERE command = ?
            """,
            ("ls",),
        ).fetchone()

    assert row == ("ls", "/usr/bin/ls")

def test_get_inventory(tmp_path):
    database = tmp_path / "test.db"

    initialize_database(database)

    inventory = CommandInventory(
        command="ls",
        path="/usr/bin/ls",
    )

    save_inventory(database, inventory)

    result = get_inventory(database, "ls")

    assert result is not None
    assert result.command == "ls"
    assert result.path == "/usr/bin/ls"


def clear_commands(database):
    with sqlite3.connect(database) as connection:
        connection.execute("DELETE FROM commands")
