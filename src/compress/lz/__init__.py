"""
This module is used as an API for developers to encode and decode data with the Lempel-Ziv algorithm.
"""
import sys
from typing import Optional, Type

from bitarray import bitarray

from compress.common import CompressionAlgorithm, Decoder, Encoder

_STRING_ENCODING = 'UTF-8'


class LZEncode(Encoder):
    """
    Compressor that can can be modified in constructor arguments.
    Functions as the API for compression process.
    Uses the Lempel-Ziv encoding algorithm to compress data.
    """

    def __init__(
            self,
            *,
            search_buffer_size: int = 255,
            lookahead_buffer_size: int = 128,
    ):
        super().__init__()
        if lookahead_buffer_size > search_buffer_size:
            raise RuntimeError
        self.search_buffer_size = search_buffer_size
        self.lookahead_buffer_size = lookahead_buffer_size

    def encode(self, data: bytes) -> bytes:
        """
        Function to call to provide input for the compressor to compress.
        Returns the compressed bytes.
        """
        encoding_process = _EncodingProcess(self, data)
        return encoding_process.encode()


class LZDecode(Decoder):

    def decode(self, data: bytes) -> bytes:
        pass


class LZ(CompressionAlgorithm):
    """
    Compressor that can can be modified in constructor arguments.
    Functions as the API for compression process.
    """

    @classmethod
    def get_encoder(cls) -> Type[Encoder]:
        return LZEncode

    @classmethod
    def get_decoder(cls) -> Type[Decoder]:
        return LZDecode


class _EncodingProcess:
    """
    Protected class to maintain the internal state of a single compression run.
    """

    def __init__(self, compressor: Encoder, data: bytes):
        super().__init__()
        self._compressor = compressor
        self._original_data = data
        self._cursor = -1
        self._matches: dict[str, list[int]] = {}

    def _find_longest_match(self) -> tuple[int, int]:
        character = self.original_data[self._cursor]
        match_indices = self.get_match(character)
        if match_indices is None or match_indices[-1] < self.search_limit():
            self.set_match(character, self._cursor)
            return 0, 0
        longest_match_offset = 0
        longest_match_length = 0
        for match_index in match_indices:
            if match_index < self.search_limit():
                continue
            left_offset = self._cursor - match_index
            for lookahead_pointer in range(
                    min(self._cursor + 1, self.data_length - 1),
                    self.lookahead_limit() + 1
            ):
                next_char_offset = lookahead_pointer - self._cursor
                if match_index + next_char_offset >= self._cursor:
                    break
                if self.original_data[lookahead_pointer] != self.original_data[match_index + next_char_offset]:
                    break
                match_length = lookahead_pointer - self._cursor
                if longest_match_length <= match_length:
                    longest_match_offset = left_offset
                    longest_match_length = match_length
        self.set_match(character, self._cursor)
        return longest_match_offset, longest_match_length

    def encode(self) -> bytes:
        """
        Used to start the encoding process internally.
        """
        encoded_buffer = bytearray()
        self._cursor = 0
        while self._cursor < self.data_length:
            left_offset, match_length = self._find_longest_match()
            encoded_buffer.extend(match_length.to_bytes(length=1, byteorder=sys.byteorder, signed=False))
            if match_length == 0:
                encoded_buffer.extend(
                    self.original_data[self._cursor].to_bytes(length=1, byteorder=sys.byteorder, signed=False))
                self._cursor += 1
            else:
                encoded_buffer.extend(left_offset.to_bytes(length=1, byteorder=sys.byteorder, signed=False))
                self._cursor += match_length
        return encoded_buffer

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
