from dataclasses import dataclass
from termly.commands import get_available_commands, get_best_command
from termly.confidence import calculate_confidence

@dataclass
class Suggestion:
	title: str
	explanation: str
	command: str | None = None

def suggest(error_info):
	if error_info is None:
		return None
	if error_info.error_type == "missing_path":
		return Suggestion(
			title="Check the path",
            		explanation="The file or directory you entered does not exist.",
            		command="ls"
		)
	if error_info.error_type == "permission_denied":
		return Suggestion(
			title="Check permissions",
           		explanation="You dont have permission to do this operation.",
 		)
	if error_info.error_type == "command_not_found":
		command = error_info.message.split(":")[0]
		available_commands = get_available_commands()

		match = get_best_command(command, available_commands)
		confidence = calculate_confidence(match)

		if match:
			best_command=match.command
			if confidence>=75:
				title = f"Did you mean: {best_command}?"
			else:
				title = f"Possible match: {best_command}?"

			return Suggestion(
				title=title,
				explanation=f"Termly confidence ({confidence:.0f}%)",
				command = best_command
			)

		return Suggestion(
			title="Unknown error",
			explanation="Termly doesn't know how to help with yet"
		)

