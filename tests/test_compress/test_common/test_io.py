import os
import uuid

import pytest

from compress.common import io


def test_read_file():
    result = io.read_file('sample/lorem.txt')
    assert result is not None


def test_read_invalid_file():
    with pytest.raises(IOError):
        io.read_file(f'sample/{str(uuid.uuid4())}')


def test_write_file():
    file_path = f'temp/{str(uuid.uuid4())}'
    data_written = str(uuid.uuid4()).encode()
    result = io.write_file(file_path, data_written)
    assert result == file_path
    assert data_written == io.read_file(file_path)
    os.remove(file_path)


def test_write_file_exists():
    file_path = f'temp/{str(uuid.uuid4())}'
    data_written = str(uuid.uuid4()).encode()
    result = io.write_file(file_path, data_written)
    with pytest.raises(FileExistsError):
        io.write_file(file_path, data_written)
    os.remove(file_path)

