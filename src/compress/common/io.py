"""
This module is used to read and write files.
"""
import os
from typing import Optional


def read_file(file_path: str) -> Optional[bytes]:
    """
    This function is used to read files.
    """
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except IOError:
        print(f'Could not read file {file_path}')


def write_file(file_path: str, data: bytes):
    """
    This function is used to write files.
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'xb') as file:
            file.seek(0)
            file.write(data)
    except FileExistsError:
        print(f'File {file_path} already exists')
        raise
    except IOError:
        print(f'Could not write to file {file_path}')
    else:
        return file_path
