import random
import uuid

from compress.common import convert


def test_int_to_bytes():
    num = 0
    assert convert.int_to_bytes(num) == b'\x00' * 4


def test_bytes_to_int():
    byte_data = b'\0' * 4
    assert convert.bytes_to_int(byte_data) == 0


def test_int_to_bytes_back():
    num = random.randint(0, 100)
    assert convert.bytes_to_int(convert.int_to_bytes(num)) == num


def test_bytes_to_int_back():
    byte_data = str(uuid.uuid4()).encode()[0:4]
    assert convert.int_to_bytes(convert.bytes_to_int(byte_data)) == byte_data


def test_char_int_to_bytes():
    num = ord("0")
    assert convert.char_int_to_bytes(num) == b'0'


def test_bytes_to_char_int():
    byte_data = b'0'
    assert convert.bytes_to_int(byte_data) == ord('0')


def test_char_int_to_bytes_back():
    num = random.randint(0, 100)
    assert convert.bytes_to_char_int(convert.char_int_to_bytes(num)) == num


def test_bytes_to_char_int_back():
    byte_data = str(uuid.uuid4()).encode()[0:1]
    assert convert.char_int_to_bytes(convert.bytes_to_char_int(byte_data)) == byte_data
