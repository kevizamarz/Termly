import subprocess


HELP_TIMEOUT = 5


def get_help(command):
    try:
        result = subprocess.run(
            [command, "--help"],
            capture_output=True,
            text=True,
            timeout=HELP_TIMEOUT,
        )

        if result.returncode == 0:
            return result.stdout

        return result.stdout or result.stderr

    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
