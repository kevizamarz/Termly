from termly.runner import run_command


def test_successful_command():
    result = run_command(["echo", "hello"])

    assert result.exit_code == 0
    assert result.stdout.strip() == "hello"
    assert result.stderr == ""


def test_command_not_found():
    result = run_command(["this_command_does_not_exist"])

    assert result.exit_code == 127
    assert "command not found" in result.stderr


def test_command_with_error():
    result = run_command(["ls", "/this/path/does/not/exist"])

    assert result.exit_code != 0
    assert "No such file" in result.stderr
