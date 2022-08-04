"""
This module is used as an API for developers to encode and decode data with LZ77.
"""
from typing import Optional

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
        if lookahead_buffer_size > search_buffer_size:
            raise RuntimeError
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
        self._matches: dict[str, list[int]] = {}

    def encode(self) -> str:
        """
        Used to start the encoding process internally.
        """
        encoded_buffer = bytearray()
        index = 0
        while index < self.data_length:
            match_buffer = self.original_data[index:index + 1]
            match_indices = self.get_match(match_buffer)
            self.set_match(match_buffer, index)
            left_offset = 0
            match_length = 0
            if match_indices is not None:
                longest_match_offset = index - match_indices[-1]
                longest_match = match_buffer
                for match_index in match_indices:
                    match_buffer = self.original_data[index:index + 1]
                    for lookahead_pointer in range(
                            min(index + 1, self.data_length - 1),
                            self.lookahead_limit() + 1
                    ):
                        next_char_index = lookahead_pointer - index
                        if match_index + next_char_index >= index:
                            break
                        if self.original_data[lookahead_pointer] != self.original_data[match_index + next_char_index]:
                            break
                        left_offset = index - match_index
                        match_buffer += self.original_data[lookahead_pointer: lookahead_pointer + 1]
                        if len(longest_match) <= len(match_buffer):
                            longest_match = match_buffer
                            longest_match_offset = left_offset
                match_length = len(longest_match)
                left_offset = longest_match_offset
            encoded_buffer.append(match_length)
            if match_length == 0:
                encoded_buffer.append(self.original_data[index])
                index += 1
            else:
                encoded_buffer.append(left_offset)
                index += match_length
        return encoded_buffer.decode(encoding=_STRING_ENCODING)

    def set_match(self, key, index: int):
        if self._matches.get(key, None) is None:
            self._matches[key] = [index]
            return
        self._matches[key].append(index)

    def get_match(self, key) -> Optional[list[int]]:
        if key not in self._matches:
            return None
        return self._matches[key].copy()

    @property
    def original_data(self):
        return self._original_data

    @property
    def data_length(self):
        return len(self.original_data)

    def search_limit(self):
        """
        Returns the smallest index of the search buffer.
        """
        return max(self._cursor - self._compressor.search_buffer_size, 0)

    def lookahead_limit(self):
        """
        Returns the largest index of the lookahead buffer.
        """
        return min(self._cursor + self._compressor.lookahead_buffer_size, self.data_length - 1)

    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, value: int):
        self._cursor = value
