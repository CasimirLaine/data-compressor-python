from lz import LZCompressor


def test_compressor_params():
    search_buffer_size = 5
    lookahead_buffer_size = 10
    compressor = LZCompressor(
        search_buffer_size=search_buffer_size,
        lookahead_buffer_size=lookahead_buffer_size
    )
    assert compressor.search_buffer_size == search_buffer_size
    assert compressor.lookahead_buffer_size == lookahead_buffer_size
