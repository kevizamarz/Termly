from dataclasses import dataclass

from rapidfuzz.fuzz import ratio


@dataclass
class KnowledgeMatch:
    knowledge: object
    score: float


def calculate_keyword_score(question, knowledge):
    stop_words = {
        "how",
        "do",
        "i",
        "the",
        "a",
        "an",
        "is",
        "are",
        "to",
        "me",
        "can",
        "what",
        "where",
        "please",
    }

    words = {
        word.lower()
        for word in question.split()
        if word.lower() not in stop_words
    }

    keywords = {
        keyword.lower()
        for keyword in knowledge.keywords
    }

    if not words:
        return 0

    matches = words & keywords

    return (len(matches) / len(words)) * 100


def calculate_score(question, knowledge):
    phrase_score = 0

    for phrase in knowledge.phrases:
        score = ratio(question, phrase)

        if score > phrase_score:
            phrase_score = score

    keyword_score = calculate_keyword_score(question, knowledge)

    return (phrase_score * 0.7) + (keyword_score * 0.3)


def find_best_match(question, provider):
    best_knowledge = None
    best_score = 0

    for knowledge in provider.get_commands():
        score = calculate_score(question, knowledge)

        if score > best_score:
            best_score = score
            best_knowledge = knowledge

    if best_score >= 50:
        return KnowledgeMatch(
            knowledge=best_knowledge,
            score=best_score,
        )

    return None
