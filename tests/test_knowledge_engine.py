from termly.knowledge_engine import find_best_match


def test_finds_list_directory():
    match = find_best_match("how do I see the files")

    assert match is not None
    assert match.knowledge.intent == "list_directories"
    assert match.knowledge.command == "ls"


def test_finds_change_directory():
    match = find_best_match("how do I go to folder")

    assert match is not None
    assert match.knowledge.intent == "change_directory"
    assert match.knowledge.command == "cd"


def test_returns_score():
    match = find_best_match("list files")

    assert match is not None
    assert match.score > 0


def test_returns_none_for_unknown_question():
    match = find_best_match("how do I configure a firewall")

    assert match is None

def test_understands_natural_list_files_question():
    match = find_best_match("how do I see the files")

    assert match is not None
    assert match.knowledge.intent == "list_directories"


def test_rejects_unrelated_question():
    match = find_best_match("how do I configure a firewall")

    assert match is None
