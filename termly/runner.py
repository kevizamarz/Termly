from dataclasses import dataclass
import subprocess

@dataclass
class CommandResult:
	stdout: str
	stderr: str
	exit_code: int

def run_command(command):
	try:
		result = subprocess.run(command, capture_output=True, text=True)
		return CommandResult (
			stdout = result.stdout,
			stderr = result.stderr,
			exit_code = result.returncode
		)
	except FileNotFoundError:
		return CommandResult(
			stdout="",
			stderr=f"{command[0]}: command not found",
			exit_code=127
		)



