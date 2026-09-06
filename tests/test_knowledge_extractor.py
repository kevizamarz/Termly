from termly.knowledge_extractor import extract_knowledge


def test_extracts_command_description():
    help_text = """Usage: chmod [OPTION]... MODE FILE...
Change the mode of each FILE to MODE.

-c, --changes
    like verbose but report only when a change is made
"""

    knowledge = extract_knowledge("chmod", help_text)

    assert knowledge.command == "chmod"
    assert knowledge.description == "Change the mode of each FILE to MODE."
    assert knowledge.help_text == help_text
    assert knowledge.source == "help"

def test_extracts_keywords():
    help_text = """Usage: chmod [OPTION]... MODE FILE...
Change the mode of each FILE to MODE.

-c, --changes
    like verbose but report only when a change is made
"""

    knowledge = extract_knowledge("chmod", help_text)

    assert "change" in knowledge.keywords
    assert "mode" in knowledge.keywords
    assert "file" in knowledge.keywords

def test_extracts_searchable_phrase():
    help_text = """Usage: chmod [OPTION]... MODE FILE...
Change the mode of each FILE to MODE.
"""

    knowledge = extract_knowledge("chmod", help_text)

    assert "change the mode of each file to mode" in knowledge.phrases
