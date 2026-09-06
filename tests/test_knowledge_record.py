from termly.knowledge_model import CommandKnowledge


def test_command_knowledge():
    knowledge = CommandKnowledge(
        command="ls",
        phrases=["list files"],
        keywords=["list", "files"],
        description="Lists all the files",
        example="ls",
        help_text="Usage: ls [OPTION]...",
        source="help",
    )

    assert knowledge.command == "ls"
    assert knowledge.help_text == "Usage: ls [OPTION]..."
    assert knowledge.source == "help"
