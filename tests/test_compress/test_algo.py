import os
import random
import string
import uuid

import pytest

from compress import huffman
from compress.common import io
from test_compress import ROOT_PATH

__N = [10_000, 100_000, 1_000_000, 10_000_000]

__ALGORITHMS = [
    huffman.Huffman,
    # lz.LZ,
]

__FILES = [
    'sample/simple.txt',
    'sample/lorem.txt',
    'sample/big_image.jpg',
    'sample/small_image.jpeg',
    'sample/image.png',
]


def _gen_combinations():
    combinations = []
    for a in __ALGORITHMS:
        for n in __N:
            combinations.append((a, n))
    return combinations


def _gen_file_combinations():
    combinations = []
    for a in __ALGORITHMS:
        for f in __FILES:
            combinations.append((a, f))
    return combinations


def _random_bytes(n):
    return ''.join(random.choice(string.printable) for _ in range(n)).encode()


@pytest.mark.parametrize("algorithm, n", _gen_combinations())
def test_encode_smaller(algorithm, n):
    encoder = algorithm.get_encoder()
    input_bytes = _random_bytes(n)
    compressor = encoder()
    result = compressor.encode(input_bytes)
    assert len(result) <= len(input_bytes)


@pytest.mark.parametrize("algorithm, n", _gen_combinations())
def test_encode_smaller_enough(algorithm, n):
    encoder = algorithm.get_encoder()
    input_bytes = _random_bytes(n)
    compressor = encoder()
    result = compressor.encode(input_bytes)
    assert len(result) <= len(input_bytes) * 0.9


@pytest.mark.parametrize("algorithm, n", _gen_combinations())
def test_decode_same_length(algorithm, n):
    encoder, decoder = (algorithm.get_encoder(), algorithm.get_decoder())
    input_bytes = _random_bytes(n)
    compressor = encoder()
    result = compressor.encode(input_bytes)
    decompressor = decoder()
    decoded_bytes = decompressor.decode(result)
    assert len(input_bytes) == len(decoded_bytes)


@pytest.mark.parametrize("algorithm, n", _gen_combinations())
def test_decode(algorithm, n):
    encoder, decoder = (algorithm.get_encoder(), algorithm.get_decoder())
    input_bytes = _random_bytes(n)
    compressor = encoder()
    result = compressor.encode(input_bytes)
    decompressor = decoder()
    decoded_bytes = decompressor.decode(result)
    assert input_bytes == decoded_bytes


@pytest.fixture(autouse=True, scope='function')
def delete_output_files():
    def clear_output():
        sample_folder = os.path.join(ROOT_PATH, 'sample')
        for entry in os.scandir(sample_folder):
            if entry.is_file() and entry.name.endswith('.output'):
                try:
                    os.remove(entry.path)
                except FileNotFoundError:
                    pass

    clear_output()
    yield
    clear_output()


@pytest.mark.parametrize("algorithm, file", _gen_file_combinations())
def test_read_file(algorithm, file):
    file = os.path.join(ROOT_PATH, file)
    encoder, decoder = (algorithm.get_encoder(), algorithm.get_decoder())
    input_bytes = io.read_file(file)
    compressor = encoder()
    result = compressor.encode(input_bytes)
    decompressor = decoder()
    decoded_bytes = decompressor.decode(result)
    assert input_bytes == decoded_bytes


@pytest.mark.parametrize("algorithm, file", _gen_file_combinations())
def test_read_encoded_file(algorithm, file):
    file = os.path.join(ROOT_PATH, file)
    encoder, decoder = (algorithm.get_encoder(), algorithm.get_decoder())
    input_bytes = io.read_file(file)
    compressor = encoder()
    result = compressor.encode(input_bytes)
    output_path = f'{file}.{str(uuid.uuid4()).replace("-", "")}.output'
    io.write_file(output_path, result)
    compressed_bytes = io.read_file(output_path)
    assert result == compressed_bytes
    decompressor = decoder()
    decoded_bytes = decompressor.decode(compressed_bytes)
    assert input_bytes == decoded_bytes


@pytest.mark.parametrize("algorithm, file", _gen_file_combinations())
def test_read_decoded_file(algorithm, file):
    file = os.path.join(ROOT_PATH, file)
    encoder, decoder = (algorithm.get_encoder(), algorithm.get_decoder())
    input_bytes = io.read_file(file)
    compressor = encoder()
    result = compressor.encode(input_bytes)
    output_path = f'{file}.{str(uuid.uuid4()).replace("-", "")}.output'
    io.write_file(output_path, result)
    compressed_bytes = io.read_file(output_path)
    decompressor = decoder()
    decoded_bytes = decompressor.decode(compressed_bytes)
    decoded_output_path = f'{file}.{str(uuid.uuid4()).replace("-", "")}.output'
    io.write_file(decoded_output_path, decoded_bytes)
    decoded_input_bytes = io.read_file(file)
    assert input_bytes == decoded_input_bytes
