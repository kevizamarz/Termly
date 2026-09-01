from termly.analyzer import ErrorInfo, analyze


def make_result(exit_code, stderr=""):
    class Result:
        pass

    result = Result()
    result.exit_code = exit_code
    result.stderr = stderr

    return result


def test_success_returns_none():
    result = make_result(0)

    assert analyze(result) is None


def test_command_not_found():
    result = make_result(
        127,
        "bash: gti: command not found"
    )

    error = analyze(result)

    assert error.error_type == "command_not_found"


def test_missing_path():
    result = make_result(
        1,
        "ls: cannot access '/pint': No such file or directory"
    )

    error = analyze(result)

    assert error.error_type == "missing_path"


def test_permission_denied():
    result = make_result(
        1,
        "cat: /secret: Permission denied"
    )

    error = analyze(result)

    assert error.error_type == "permission_denied"


def test_unknown_error():
    result = make_result(
        1,
        "Something went wrong"
    )

    error = analyze(result)

    assert error.error_type == "unknown"
