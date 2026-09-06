from termly.cli import run


def test_command_not_found_flow(capsys):
    run(["gti"])

    output = capsys.readouterr().out

    assert "command not found" in output
    assert "git" in output

