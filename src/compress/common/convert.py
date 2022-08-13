"""
Module to perform data type conversions.
"""
import sys


def int_to_bytes(num: int) -> bytes:
    """
    Converts a 64-bit integer to bytes.
    """
    return num.to_bytes(length=4, byteorder=sys.byteorder, signed=False)


def bytes_to_int(data: bytes) -> int:
    """
    Converts four bytes to integer.
    """
    return int.from_bytes(data, byteorder=sys.byteorder, signed=False)


def char_int_to_bytes(char_code: int):
    """
    Converts a character code to a byte.
    """
    return char_code.to_bytes(length=1, byteorder=sys.byteorder)


def bytes_to_char_int(char_bytes: bytes):
    """
    Converts a byte code to a character code.
    """
    return int.from_bytes(char_bytes, byteorder=sys.byteorder)
