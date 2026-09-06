from pathlib import Path


def get_data_directory():
    return Path.home() / ".local" / "share" / "termly"


def get_database_path():
    return get_data_directory() / "termly.db"
