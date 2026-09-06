from dataclasses import dataclass


@dataclass
class CommandKnowledge:
    command: str
    phrases: list[str]
    keywords: list[str]
    description: str
    example: str
    help_text: str | None
    source: str


@dataclass
class CommandInventory:
    command: str
    path: str
