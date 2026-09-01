from termly.analyzer import ErrorInfo
from termly.suggester import suggest


def test_none_error_returns_none():
    result = suggest(None)

    assert result is None


def test_missing_path():
    error = ErrorInfo(
        error_type="missing_path",
        message="No such file or directory"
    )

    suggestion = suggest(error)

    assert suggestion.title == "Check the path"
    assert suggestion.command == "ls"


def test_permission_denied():
    error = ErrorInfo(
        error_type="permission_denied",
        message="Permission denied"
    )

    suggestion = suggest(error)

    assert suggestion.title == "Check permissions"


def test_command_not_found():
    error = ErrorInfo(
        error_type="command_not_found",
        message="gti: command not found"
    )

    suggestion = suggest(error)

    assert suggestion is not None
    assert suggestion.command == "git"


def test_unknown_error():
    error = ErrorInfo(
        error_type="something_else",
        message="Something went wrong"
    )

    suggestion = suggest(error)

    assert suggestion is None
