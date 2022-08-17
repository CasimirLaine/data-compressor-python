"""
This module is used to read and write files.
"""
import os
from typing import Optional


def read_file(file_path: str) -> Optional[bytes]:
    """
    This function is used to read files.
    """
    with open(file_path, 'rb') as file:
        return file.read()


def write_file(file_path: str, data: bytes):
    """
    This function is used to write files.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'xb') as file:
        file.seek(0)
        file.write(data)
    return file_path
