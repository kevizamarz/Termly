import sys
import re
from termly.knowledge import ANSWERS
from rapidfuzz.fuzz import ratio
from termly.runner import run_command
from termly.analyzer import analyze
from termly.suggester import suggest

def find_best_match(question):
	best_answer = None
	best_score = 0

	for answer in ANSWERS.values():
		for phrase in answer["phrases"]:
			score = ratio(question, phrase)

			if score > best_score:
				best_score = score
				best_answer = answer
	if best_score >= 50:
		return best_answer

	return None

def ask(question):
	question = question.lower()

	answer = find_best_match(question)

	if answer is None:
		print("I don't know that yet")
		return

	print(f"Try: {answer['command']}")
	print(f"What it does: {answer['description']}")
	print(f"Example:  {answer['example']}")
	return

def explain(error):
	if "No such file or directory" in error:
		print("The file you specified does not exist")
		return
	print("I dont know that yet")

def parse_error(error):
	match = re.search(r"'([^']+)'", error)
	if match:
		return match.group(1)
	return None

def analyze_error(error):
	if "No such file" in error:
		path = parse_error(error)
		print("Error type: Missing file")
		if path:
			print(f"The '{path}' entered doesn't exist")
		else:
			print("Check spelling or file path")
		return
	if "Permission denied" in error:
		print("Error type: Permission denied")
		print("Check the file permissions")
		return
	print("I dont know that yet")

def run(command):
	result = run_command(command)

	if result.exit_code == 0:
		print(result.stdout)
		return
	error = analyze(result)
	suggestion = suggest(error)

	print(result.stderr)

	if suggestion:
		print()
		print(f"Suggestion: {suggestion.title}")
		print(suggestion.explanation)
		if suggestion.command:
			print(f"try: {suggestion.command}")


def main():
	if len(sys.argv)>=3 and sys.argv[1]=="ask":
		question = " ".join(sys.argv[2:])
		ask(question)
	elif len(sys.argv)>=3 and sys.argv[1] == "explain":
		error = " ".join(sys.argv[2:])
		explain(error)
	elif len(sys.argv)>=3 and sys.argv[1]=="run":
		command = sys.argv[2:]
		run(command)
	else:
		print("Syntax: termly ask \"your question\"")



if __name__ == "__main__":
	main()

