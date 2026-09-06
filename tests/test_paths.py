from pathlib import Path

from termly.paths import get_data_directory, get_database_path


def test_get_data_directory():
    assert get_data_directory() == Path.home() / ".local" / "share" / "termly"


def test_get_database_path():
    assert get_database_path() == (
        Path.home() / ".local" / "share" / "termly" / "termly.db"
    )
