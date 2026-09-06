import sys
import re
from termly.knowledge_engine import find_best_match
from termly.runner import run_command
from termly.analyzer import analyze
from termly.suggester import suggest
from termly.knowledge_provider import KnowledgeProvider
from termly.knowledge_store import initialize_database, seed_knowledge
from termly.paths import get_database_path
from termly.knowledge import KNOWLEDGE
from termly.knowledge_updater import update_command

def ask(question, provider):
    question = question.lower()
    answer = find_best_match(question, provider)

    if answer is None:
        print("I don't know that yet")
        return

    knowledge = answer.knowledge

    print(f"Try: {knowledge.command}")
    print(f"What it does: {knowledge.description}")
    print(f"Example:  {knowledge.example}")
    print(f"Confidence: {answer.score:.0f}%")

def learn(command, database):
    knowledge = update_command(database, command)

    if knowledge is None:
        print(f"Could not learn '{command}'")
        return

    print(f"Learned: {knowledge.command}")
    print(f"What it does: {knowledge.description}")

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
    database = get_database_path()
    initialize_database(database)
    seed_knowledge(database, KNOWLEDGE)
    provider = KnowledgeProvider(database)

    if len(sys.argv) >= 3 and sys.argv[1] == "ask":
        question = " ".join(sys.argv[2:])
        ask(question, provider)
    elif len(sys.argv) >= 3 and sys.argv[1] == "learn":
        command = sys.argv[2]
        learn(command, database)
    elif len(sys.argv) >= 3 and sys.argv[1] == "explain":
        error = " ".join(sys.argv[2:])
        explain(error)
    elif len(sys.argv) >= 3 and sys.argv[1] == "run":
        command = sys.argv[2:]
        run(command)
    else:
        print('Syntax: termly ask "your question"')


if __name__ == "__main__":
	main()

