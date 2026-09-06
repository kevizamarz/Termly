from termly.knowledge import KNOWLEDGE
from termly.knowledge_engine import find_best_match
from termly.knowledge_provider import KnowledgeProvider
from termly.knowledge_store import initialize_database, save_command


def create_provider(tmp_path):
    database = tmp_path / "termly.db"

    initialize_database(database)

    for knowledge in KNOWLEDGE:
        save_command(database, knowledge)

    return KnowledgeProvider(database)


def test_finds_list_directory(tmp_path):
    provider = create_provider(tmp_path)

    match = find_best_match("how do I see the files", provider)

    assert match is not None
    assert match.knowledge.command == "ls"


def test_finds_change_directory(tmp_path):
    provider = create_provider(tmp_path)

    match = find_best_match("how do I go to folder", provider)

    assert match is not None
    assert match.knowledge.command == "cd"


def test_returns_score(tmp_path):
    provider = create_provider(tmp_path)

    match = find_best_match("list files", provider)

    assert match is not None
    assert match.score > 0


def test_returns_none_for_unknown_question(tmp_path):
    provider = create_provider(tmp_path)

    match = find_best_match(
        "how do I configure a firewall",
        provider,
    )

    assert match is None


def test_understands_natural_list_files_question(tmp_path):
    provider = create_provider(tmp_path)

    match = find_best_match(
        "how do I see the files",
        provider,
    )

    assert match is not None
    assert match.knowledge.command == "ls"


def test_rejects_unrelated_question(tmp_path):
    provider = create_provider(tmp_path)

    match = find_best_match(
        "how do I configure a firewall",
        provider,
    )

    assert match is None
