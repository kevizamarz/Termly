import os
from dataclasses import dataclass
from rapidfuzz.fuzz import ratio
from rapidfuzz.distance import Levenshtein

@dataclass
class CommandMatch:
    command: str
    similarity: float
    distance: int

def get_available_commands():
	commands=set()

	for directory in os.environ.get("PATH", "").split(os.pathsep):
		if not os.path.isdir(directory):
			continue
		for filename in os.listdir(directory):
			path = os.path.join(directory, filename)

			if os.path.isfile(path) and os.access(path, os.X_OK):
				commands.add(filename)
	return commands

def find_similar_commands(command, available_commands, threshold=60):
	matches = []

	for candidate in available_commands:
		score = ratio(command, candidate)

		if score >= threshold:
			matches.append((candidate, score))
	matches.sort(key=lambda match: match[1], reverse=True)

	return matches

def rank_commands(command, available_commands):
	ranked = []

	for candidate in available_commands:
		similarity = ratio(command, candidate)
		distance = Levenshtein.distance(command, candidate)

		ranked.append(
			CommandMatch(
				command=candidate,
				similarity= similarity,
				distance= distance
				)
		)
	ranked.sort(key=lambda item: (item.distance, -item.similarity))
	return ranked

def get_best_command(command, available_commands, threshold=65, margin=0):
	ranked = rank_commands(command, available_commands)

	if not ranked:
		return None

	best_match = ranked [0]

	if best_match.similarity < threshold:
		return None

	if len(ranked)>1:
		second_match = ranked[1]
		if best_match.similarity - second_match.similarity < margin:
			return None
	return best_match

