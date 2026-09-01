from termly.commands import get_available_commands, get_best_command

def test_git_typo():
	commands = get_available_commands()
	match = get_best_command("gti", commands)

	assert match is not None
	assert match.command == "git"
