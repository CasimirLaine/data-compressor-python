import sys


def int_to_bytes(num: int) -> bytes:
    return num.to_bytes(length=4, byteorder=sys.byteorder, signed=False)


def bytes_to_int(data: bytes) -> int:
    return int.from_bytes(data, byteorder=sys.byteorder, signed=False)
