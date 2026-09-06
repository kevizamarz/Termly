import json
import sqlite3

from termly.paths import get_data_directory


def initialize_database(database):
    get_data_directory().mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(database) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS commands (
                command TEXT PRIMARY KEY,
                phrases TEXT NOT NULL,
                keywords TEXT NOT NULL,
                description TEXT NOT NULL,
                example TEXT NOT NULL,
                help_text TEXT,
                source TEXT NOT NULL
            )
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS command_inventory (
                command TEXT PRIMARY KEY,
                path TEXT NOT NULL
            )
            """
        )


def save_command(database, knowledge):
    with sqlite3.connect(database) as connection:
        connection.execute(
            """
            INSERT INTO commands (
                command,
                phrases,
                keywords,
                description,
                example,
                help_text,
                source
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(command) DO UPDATE SET
                phrases = excluded.phrases,
                keywords = excluded.keywords,
                description = excluded.description,
                example = excluded.example,
                help_text = excluded.help_text,
                source = excluded.source
            """,
            (
                knowledge.command,
                json.dumps(knowledge.phrases),
                json.dumps(knowledge.keywords),
                knowledge.description,
                knowledge.example,
                knowledge.help_text,
                knowledge.source,
            ),
        )


def save_inventory(database, inventory):
    with sqlite3.connect(database) as connection:
        connection.execute(
            """
            INSERT INTO command_inventory (
                command,
                path
            )
            VALUES (?, ?)
            ON CONFLICT(command) DO UPDATE SET
                path = excluded.path
            """,
            (
                inventory.command,
                inventory.path,
            ),
        )


def get_inventory(database, command):
    with sqlite3.connect(database) as connection:
        connection.row_factory = sqlite3.Row

        row = connection.execute(
            """
            SELECT command, path
            FROM command_inventory
            WHERE command = ?
            """,
            (command,),
        ).fetchone()

    if row is None:
        return None

    from termly.knowledge_model import CommandInventory

    return CommandInventory(
        command=row["command"],
        path=row["path"],
    )


def get_command(database, command):
    with sqlite3.connect(database) as connection:
        connection.row_factory = sqlite3.Row

        row = connection.execute(
            """
            SELECT
                command,
                phrases,
                keywords,
                description,
                example,
                help_text,
                source
            FROM commands
            WHERE command = ?
            """,
            (command,),
        ).fetchone()

    if row is None:
        return None

    from termly.knowledge_model import CommandKnowledge

    return CommandKnowledge(
        command=row["command"],
        phrases=json.loads(row["phrases"]),
        keywords=json.loads(row["keywords"]),
        description=row["description"],
        example=row["example"],
        help_text=row["help_text"],
        source=row["source"],
    )


def get_commands(database):
    with sqlite3.connect(database) as connection:
        connection.row_factory = sqlite3.Row

        rows = connection.execute(
            """
            SELECT
                command,
                phrases,
                keywords,
                description,
                example,
                help_text,
                source
            FROM commands
            ORDER BY command
            """
        ).fetchall()

    from termly.knowledge_model import CommandKnowledge

    return [
        CommandKnowledge(
            command=row["command"],
            phrases=json.loads(row["phrases"]),
            keywords=json.loads(row["keywords"]),
            description=row["description"],
            example=row["example"],
            help_text=row["help_text"],
            source=row["source"],
        )
        for row in rows
    ]


def seed_knowledge(database, knowledge):
    for entry in knowledge:
        save_command(database, entry)
