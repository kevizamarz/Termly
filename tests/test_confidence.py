from termly.commands import CommandMatch
from termly.confidence import calculate_confidence


def test_no_match_has_zero_confidence():
    confidence = calculate_confidence(None)

    assert confidence == 0


def test_exact_match_gets_high_confidence():
    match = CommandMatch(
        command="ls",
        similarity=100,
        distance=0
    )

    confidence = calculate_confidence(match)

    assert confidence == 100


def test_one_character_typo_gets_bonus():
    match = CommandMatch(
        command="ls",
        similarity=80,
        distance=1
    )

    confidence = calculate_confidence(match)

    assert confidence == 85
