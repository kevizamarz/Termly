from dataclasses import dataclass
from rapidfuzz.fuzz import ratio
from termly.knowledge import KNOWLEDGE

@dataclass
class KnowledgeMatch:
	knowledge: object
	score: float

def find_best_match(question):
    best_knowledge = None
    best_score = 0

    for knowledge in KNOWLEDGE:
        for phrase in knowledge.phrases:
            score = ratio(question, phrase)

            if score > best_score:
                best_score = score
                best_knowledge = knowledge

    if best_score >= 50:
        return KnowledgeMatch(
		knowledge = best_knowledge,
		score = best_score
	)

    return None
