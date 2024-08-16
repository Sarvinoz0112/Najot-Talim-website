# context manager for open
import contextlib
import json


@contextlib.contextmanager
def open_file(filename: str, mode: str = 'r') -> object:
    file = open(filename, mode)
    yield file
    file.close()


def read_data(filename: str):
    with open_file(filename) as f:
        return json.load(f)
