"""
This module is used as an API for developers to encode and decode data with the Lempel-Ziv algorithm.
"""
from typing import Optional, Type

from bitarray import bitarray

from compress.common import CompressionAlgorithm, Decoder, Encoder, convert

_STRING_ENCODING = 'UTF-8'


class LZEncoder(Encoder):
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
        encoding_process = _LZEncodingProcess(self, data)
        return encoding_process.encode()


class LZDecoder(Decoder):

    def decode(self, data: bytes) -> bytes:
        decoding_process = _LZDecodingProcess(self, data)
        return decoding_process.decode()


class LZ(CompressionAlgorithm):
    """
    Compressor that can can be modified in constructor arguments.
    Functions as the API for compression process.
    """

    @classmethod
    def get_encoder(cls) -> Type[Encoder]:
        return LZEncoder

    @classmethod
    def get_decoder(cls) -> Type[Decoder]:
        return LZDecoder


class _LZEncodingProcess:
    """
    Protected class to maintain the internal state of a single compression run.
    """

    def __init__(self, compressor: LZEncoder, data: bytes):
        self._encoder = compressor
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
            encoded_buffer.extend(convert.char_int_to_bytes(match_length))
            if match_length == 0:
                encoded_buffer.extend(
                    convert.char_int_to_bytes(self.original_data[self._cursor]))
                self._cursor += 1
            else:
                encoded_buffer.extend(convert.char_int_to_bytes(left_offset))
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
        return max(self._cursor - self._encoder.search_buffer_size, 0)

    def lookahead_limit(self):
        """
        Returns the largest index of the lookahead buffer.
        """
        return min(self._cursor + self._encoder.lookahead_buffer_size, self.data_length - 1)


class _LZDecodingProcess:

    def __init__(self, decoder: LZDecoder, data: bytes):
        self._decoder = decoder
        self._original_data = data
        self._cursor = -1

    def decode(self) -> bytes:
        data_in_bits = bitarray()
        data_in_bits.frombytes(self._original_data)
        output_buffer = bytearray()
        self._cursor = 0
        while self._cursor < len(data_in_bits):
            match_length = convert.bytes_to_char_int(bytes(data_in_bits[self._cursor: self._cursor + 8]))
            character_or_offset = bytes(data_in_bits[self._cursor + 8: self._cursor + 16])
            if match_length == 0:
                output_buffer.extend(character_or_offset)
            else:
                character_or_offset_int = convert.bytes_to_char_int(character_or_offset)
                output_buffer.extend(bytes(output_buffer[len(output_buffer) - character_or_offset_int: len(
                    output_buffer) - character_or_offset_int + match_length]))
            self._cursor += 16
        return bytes(output_buffer)
