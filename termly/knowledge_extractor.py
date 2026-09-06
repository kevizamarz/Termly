import re

from termly.knowledge_model import CommandKnowledge

def extract_phrases(description):
    phrase = description.lower().strip().rstrip(".")
    return [phrase]

STOP_WORDS = {
    "a", "an", "and", "as", "at", "by", "for",
    "from", "in", "is", "it", "of", "on", "or",
    "the", "to", "with",
}


def extract_keywords(text):
    words = re.findall(r"[a-zA-Z]+", text.lower())

    return [
        word
        for word in words
        if word not in STOP_WORDS
    ]


def extract_knowledge(command, help_text):
    lines = help_text.splitlines()

    description = ""

    usage_found = False

    for line in lines:
        line = line.strip()

        if line.startswith("Usage:"):
            usage_found = True
            continue

        if usage_found and line and not line.startswith("or:"):
            description = line
            break

    return CommandKnowledge(
        command=command,
        phrases=extract_phrases(description),
        keywords=extract_keywords(description),
        description=description,
        example=command,
        help_text=help_text,
        source="help",
    )
