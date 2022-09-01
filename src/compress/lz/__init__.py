"""
This module is used as an API for developers to encode and decode data with the Lempel-Ziv algorithm.
"""
from collections import deque
from typing import Optional, Type

from bitarray import bitarray

from compress.common import CompressionAlgorithm, Decoder, Encoder, convert


class LZEncoder(Encoder):
    """
    Functions as the API for compression process.
    Uses the Lempel-Ziv encoding algorithm to compress data.
    """

    def encode(self, data: bytes) -> bytes:
        """
        Function to call to provide input for the compressor to compress.
        Returns the compressed bytes.
        """
        encoding_process = _LZEncodingProcess(self, data)
        return encoding_process.encode()


class LZDecoder(Decoder):
    """
    Functions as the API for decompression process.
    Uses the Lempel-Ziv encoding algorithm to decompress data.
    """

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
        self._matches: dict[bytes, int] = {}
        self._match_indices = deque()

    def _find_longest_match(
            self,
            index: int,
            data_bytes: bytes,
            longest_match_length: int = 0,
            longest_match_offset: int = 0
    ) -> tuple[int, int]:
        """
        Finds the longest match in the search buffer.
        """
        match_index = self.get_match(data_bytes)
        if match_index is None:
            self.set_match(data_bytes, index - longest_match_length)
            return longest_match_length, longest_match_offset
        longest_match_offset = index - match_index - longest_match_length
        longest_match_length += 1
        index += 1
        if index < self.data_length:
            return self._find_longest_match(
                index,
                data_bytes + self.get_byte(index),
                longest_match_length=longest_match_length,
                longest_match_offset=longest_match_offset
            )
        return longest_match_length, longest_match_offset

    def encode(self) -> bytes:
        """
        Used to start the encoding process internally.
        """
        encoded_buffer = bitarray()
        index = 0
        while index < self.data_length:
            found_byte = self.get_byte(index)
            match_length, left_offset = self._find_longest_match(index, found_byte)
            encoded_buffer.frombytes(convert.char_int_to_bytes(match_length))
            encoded_buffer.frombytes(convert.char_int_to_bytes(left_offset))
            index += match_length
            if index < self.data_length:
                byte_to_write = convert.char_int_to_bytes(self.original_data[index])
                encoded_buffer.frombytes(byte_to_write)
            index += 1
            while self._match_indices:
                item = self._match_indices[0]
                if item[0] < index - 255:
                    del self._matches[item[1]]
                    self._match_indices.popleft()
                else:
                    break
        return bytes(encoded_buffer)

    def set_match(self, key, index: int):
        self._match_indices.append((index, key))
        self._matches[key] = index

    def get_match(self, key) -> Optional[int]:
        return self._matches.get(key, None)

    def get_byte(self, index: int) -> bytes:
        return convert.char_int_to_bytes(self.original_data[index])

    @property
    def original_data(self):
        """
        The input data to be encoded.
        """
        return self._original_data

    @property
    def data_length(self):
        """
        The size of the input data to be encoded.
        """
        return len(self.original_data)


class _LZDecodingProcess:

    def __init__(self, decoder: LZDecoder, data: bytes):
        self._decoder = decoder
        self._original_data = data
        self._cursor = -1

    def decode(self) -> bytes:
        """
        Performs the decoding of the input data.
        """
        data_in_bits = bitarray()
        data_in_bits.frombytes(self._original_data)
        output_buffer = bytearray()
        self._cursor = 0
        while self._cursor < len(data_in_bits):
            match_length = convert.bytes_to_char_int(bytes(data_in_bits[self._cursor: self._cursor + 8]))
            offset = convert.bytes_to_char_int(bytes(data_in_bits[self._cursor + 8: self._cursor + 16]))
            if match_length > 0:
                bytes_to_write = bytes(output_buffer[len(output_buffer) - offset: len(
                    output_buffer) - offset + match_length])
                output_buffer.extend(bytes_to_write)
            self._cursor += 16
            if self._cursor + 8 <= len(data_in_bits):
                byte_data = bytes(data_in_bits[self._cursor: self._cursor + 8])
                output_buffer.extend(byte_data)
            self._cursor += 8
        return bytes(output_buffer)
