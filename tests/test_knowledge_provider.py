from termly.knowledge_model import CommandKnowledge
from termly.knowledge_provider import KnowledgeProvider
from termly.knowledge_store import initialize_database, save_command


def test_provider_gets_command(tmp_path):
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

    provider = KnowledgeProvider(database)

    result = provider.get_command("ls")

    assert result is not None
    assert result.command == "ls"
    assert result.help_text == "List information"
    assert result.source == "help"


def test_provider_returns_none_for_unknown_command(tmp_path):
    database = tmp_path / "termly.db"

    initialize_database(database)

    provider = KnowledgeProvider(database)

    result = provider.get_command("does_not_exist")

    assert result is None
