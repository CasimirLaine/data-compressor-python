"""
This module is used as an API for developers to encode and decode data with LZ77.
"""
_STRING_ENCODING = 'UTF-8'


class LZCompressor:
    """
    Compressor that can can be modified in constructor arguments.
    Functions as the API for compression process.
    """

    def __init__(
            self,
            *,
            search_buffer_size: int,
            lookahead_buffer_size: int,
    ):
        super().__init__()
        self.search_buffer_size = search_buffer_size
        self.lookahead_buffer_size = lookahead_buffer_size

    def encode(self, data: str):
        """
        Function to call to provide input for the compressor to compress.
        Returns the compressed text.
        """
        encoding_process = _EncodingProcess(self, data)
        return encoding_process.encode()


class _EncodingProcess:
    """
    Protected class to maintain the internal state of a single compression run.
    """

    def __init__(self, compressor: LZCompressor, data: str):
        super().__init__()
        self._compressor = compressor
        self._original_data = data.encode(encoding=_STRING_ENCODING)
        self._cursor = -1

    def encode(self) -> str:
        """
        Used to start the encoding process internally.
        """
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

    def search_limit(self):
        """
        Returns the smallest index of the search buffer.
        """

        return max(self._cursor - self._compressor.search_buffer_size, 0)

    def lookahead_limit(self):
        """
        Returns the largest index of the lookahead buffer.
        """
        return min(self._cursor + self._compressor.lookahead_buffer_size, len(self._original_data))
