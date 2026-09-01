def calculate_confidence(match):
    if match is None:
        return 0

    score = match.similarity

    if match.distance == 0:
        score += 10
    elif match.distance == 1:
        score += 5

    return min(score, 100)
