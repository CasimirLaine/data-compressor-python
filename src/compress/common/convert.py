"""
Module to perform data type conversions.
"""
import sys


def int_to_bytes(num: int) -> bytes:
    """
    Converts a 64-bit integer to bytes.
    """
    return num.to_bytes(length=4, byteorder='big', signed=False)


def bytes_to_int(data: bytes) -> int:
    """
    Converts four bytes to integer.
    """
    return int.from_bytes(data, byteorder='big', signed=False)


def tuple_int_to_bytes(value: int):
    """
    Converts a character code to a byte.
    """
    return value.to_bytes(length=2, byteorder='big', signed=False)


def char_int_to_bytes(char_code: int):
    """
    Converts a character code to a byte.
    """
    return char_code.to_bytes(length=1, byteorder='big', signed=False)


def bytes_to_char_int(char_bytes: bytes):
    """
    Converts a byte code to a character code.
    """
    return int.from_bytes(char_bytes, byteorder='big', signed=False)
