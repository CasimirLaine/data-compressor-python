_STRING_ENCODING = 'UTF-8'

"""
Compressor that can can be modified in constructor arguments.
Functions as the API for compression process.
"""


class LZCompressor:
    def __init__(
            self,
            *,
            search_buffer_size: int,
            lookahead_buffer_size: int,
    ):
        super().__init__()
        self.search_buffer_size = search_buffer_size
        self.lookahead_buffer_size = lookahead_buffer_size

    """
    Function to call to provide input for the compressor to compress.
    Returns the compressed text.
    """

    def encode(self, data: str):
        encoding_process = _EncodingProcess(self, data)
        return encoding_process.encode()


"""
Protected class to maintain the internal state of a single compression run.
"""


class _EncodingProcess:

    def __init__(self, compressor: LZCompressor, data: str):
        super().__init__()
        self._compressor = compressor
        self._original_data = data.encode(encoding=_STRING_ENCODING)
        self._cursor = -1

    """
    Used to start the encoding process internally.
    """

    def encode(self) -> str:
        encoded_bytearray = bytearray()
        index = 0
        while True:
            if index >= len(self._original_data):
                break
            character_found = self._original_data[index]
            left_offset = 0
            match_length = 0
            encoded_bytearray.append(left_offset)
            encoded_bytearray.append(match_length)
            index += match_length
            encoded_bytearray.append(self._original_data[index])
            if match_length == 0:
                index += 1
        return encoded_bytearray.decode(encoding=_STRING_ENCODING)

    """
    Returns the smallest index of the search buffer.
    """

    def search_limit(self):
        return max(self._cursor - self._compressor.search_buffer_size, 0)

    """
    Returns the largest index of the lookahead buffer.
    """

    def lookahead_limit(self):
        return min(self._cursor + self._compressor.lookahead_buffer_size, len(self._original_data))
