from dataclasses import dataclass

@dataclass
class ErrorInfo:
	error_type: str
	message: str

def analyze(command_result):
	if command_result.exit_code == 0:
		return None
	if command_result.exit_code ==127:
		return ErrorInfo(
			error_type = "command_not_found",
			message = command_result.stderr.strip()
		)
	if "No such file" in command_result.stderr:
		return ErrorInfo(
			error_type = "missing_path",
			message = command_result.stderr.strip()
		)
	if "Permission denied" in command_result.stderr:
		return ErrorInfo(
			error_type = "permission_denied",
			message = command_result.stderr.strip()
		)
	return ErrorInfo(
		error_type = "unknown",
		message = command_result.stderr.strip()
	)

