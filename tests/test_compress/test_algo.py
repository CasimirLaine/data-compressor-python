import random
import string

import pytest

from compress import huffman, lz

__N = [1_000, 10_000, 100_000, 1_000_000]

__ALGORITHMS = [
    (huffman.HuffmanEncoder, huffman.HuffmanDecoder),
    (lz.LZEncoder, lz.LZDecoder)
]


def _gen_combinations():
    combinations = []
    for n in __N:
        for a in __ALGORITHMS:
            combinations.append((n, *a))
    return combinations


def _random_bytes(n):
    return ''.join(random.choice(string.printable) for _ in range(n)).encode()


@pytest.mark.parametrize("n, encoder, decoder", _gen_combinations())
def test_encode_smaller(n, encoder, decoder):
    input_bytes = _random_bytes(n)
    compressor = encoder()
    result = compressor.encode(input_bytes)
    assert len(result) <= len(input_bytes)


@pytest.mark.parametrize("n, encoder, decoder", _gen_combinations())
def test_decode(n, encoder, decoder):
    input_bytes = _random_bytes(n)
    compressor = encoder()
    result = compressor.encode(input_bytes)
    decompressor = decoder()
    decoded_bytes = decompressor.decode(result)
    assert input_bytes == decoded_bytes
