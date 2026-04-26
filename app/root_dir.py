from os import path, getenv


def get_root_dir():
    return path.dirname(path.dirname(path.abspath(__file__)))



