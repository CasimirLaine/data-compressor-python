import uuid

import pytest

from compress import lz


def test_compressor_params():
    search_buffer_size = 10
    lookahead_buffer_size = 5
    compressor = lz.LZEncode(
        search_buffer_size=search_buffer_size,
        lookahead_buffer_size=lookahead_buffer_size
    )
    assert compressor.search_buffer_size == search_buffer_size
    assert compressor.lookahead_buffer_size == lookahead_buffer_size


def test_invalid_compressor_params():
    with pytest.raises(RuntimeError):
        compressor = lz.LZEncode(
            search_buffer_size=5,
            lookahead_buffer_size=10
        )


def test_encode_smaller():
    input_string = (str(uuid.uuid4()) * 50).encode()
    compressor = lz.LZEncode()
    result = compressor.encode(input_string)
    assert len(result) <= len(input_string)


def test_decode():
    input_string = (str(uuid.uuid4()) * 50).encode()
    compressor = lz.LZEncode()
    result = compressor.encode(input_string)
    decompressor = lz.LZDecode()
    decoded_bytes = decompressor.decode(result)
    assert input_string == decoded_bytes
