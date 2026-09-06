from termly.knowledge_engine import find_best_match


def test_finds_list_directory():
    match = find_best_match("how do I see the files")

    assert match is not None
    assert match.knowledge.intent == "list_directories"
    assert match.knowledge.command == "ls"


def test_finds_change_directory():
    match = find_best_match("how do I go to downloads")

    assert match is not None
    assert match.knowledge.intent == "change_directory"
    assert match.knowledge.command == "cd Downloads"


def test_returns_score():
    match = find_best_match("list files")

    assert match is not None
    assert match.score > 0


def test_returns_none_for_unknown_question():
    match = find_best_match("how do I configure a firewall")

    assert match is None
