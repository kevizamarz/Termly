import subprocess
from termly.documentation import get_help

def test_get_help_for_ls():
    help_text = get_help("ls")

    assert help_text is not None
    assert "Usage:" in help_text
    assert "List information" in help_text

def test_get_help_for_unknown_command():
    help_text = get_help("this_command_does_not_exist")

    assert help_text is None

def test_get_help_timeout(monkeypatch):
    def fake_run(*args, **kwargs):
        raise subprocess.TimeoutExpired(
            cmd=["fake-command", "--help"],
            timeout=5,
        )

    monkeypatch.setattr("termly.documentation.subprocess.run", fake_run)

    help_text = get_help("fake-command")

    assert help_text is None
