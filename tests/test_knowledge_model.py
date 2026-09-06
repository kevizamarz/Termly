from termly.knowledge_model import CommandKnowledge


def test_command_knowledge_creation():
    knowledge = CommandKnowledge(
        command="ls",
        phrases=["list files", "show files"],
        keywords=["list", "show", "files", "directory"],
        description="list files and directories",
        example="ls",
        help_text="List information about the FILEs",
        source="help",
    )

    assert knowledge.command == "ls"
    assert "list files" in knowledge.phrases
    assert "files" in knowledge.keywords
    assert knowledge.description == "list files and directories"
    assert knowledge.example == "ls"
    assert knowledge.help_text == "List information about the FILEs"
    assert knowledge.source == "help"
