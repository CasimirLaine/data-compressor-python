import lz

if __name__ == '__main__':
    compressor = lz.LZCompressor(
        search_buffer_size=16,
        lookahead_buffer_size=8
    )
    print(compressor.encode('test' * 100))
