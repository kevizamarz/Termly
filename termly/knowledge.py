from .knowledge_model import CommandKnowledge


KNOWLEDGE = [
    CommandKnowledge(
        command="cd",
        phrases=[
            "open folder",
            "go to directory",
            "access folder",
        ],
        keywords=[
            "open",
            "go",
            "access",
            "directory",
            "folder",
        ],
        description="Moves you into the desired folder",
        example="cd Downloads",
        help_text=None,
        source="builtin",
    ),
    CommandKnowledge(
        command="ls",
        phrases=[
            "list files",
            "show files",
            "show directory contents",
        ],
        keywords=[
            "list",
            "show",
            "files",
            "directory",
            "folder",
            "contents",
        ],
        description="Lists all the files",
        example="ls",
        help_text=None,
        source="builtin",
    ),
]
