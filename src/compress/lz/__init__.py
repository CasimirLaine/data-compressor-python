"""
This module is used as an API for developers to encode and decode data with the Lempel-Ziv algorithm.
"""
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
    Functions as the API for compression process.
    """

    @classmethod
    def get_encoder(cls) -> Type[Encoder]:
        return LZEncoder

    @classmethod
    def get_decoder(cls) -> Type[Decoder]:
        return LZDecoder


_OFFSET_BITS = 12
_LENGTH_BITS = 4


class _LZEncodingProcess:
    """
    Protected class to maintain the internal state of a single compression run.
    """

    SEARCH_LIMIT = 2 ** _OFFSET_BITS - 1
    LOOKAHEAD_LIMIT = 2 ** _LENGTH_BITS - 1

    def __init__(self, compressor: LZEncoder, data: bytes):
        self._encoder = compressor
        self._original_data = data
        self._matches: dict[bytes, int] = {}

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
        match_index = self.get_match(data_bytes, index - longest_match_length)
        self.set_match(data_bytes, index - longest_match_length)
        if match_index is None:
            return longest_match_length, longest_match_offset
        longest_match_offset = index - match_index - longest_match_length
        longest_match_length += 1
        index += 1
        if index < self.data_length and longest_match_length < self.LOOKAHEAD_LIMIT:
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
        encoded_buffer = bitarray(endian='big')
        index = 0
        while index < self.data_length:
            found_byte = self.get_byte(index)
            match_length, left_offset = self._find_longest_match(index, found_byte)
            if _LENGTH_BITS + _OFFSET_BITS + 8 <= match_length * 8:
                encoded_buffer.append(1)
                output_tuple = (match_length << _OFFSET_BITS) | left_offset
                encoded_buffer.frombytes(convert.tuple_int_to_bytes(output_tuple))
                index += match_length
                if index < self.data_length:
                    byte_to_write = self.original_data[index: index + 1]
                    encoded_buffer.frombytes(byte_to_write)
            else:
                encoded_buffer.append(0)
                encoded_buffer.frombytes(found_byte)
            index += 1
        encoded_buffer.fill()
        return bytes(encoded_buffer)

    def set_match(self, key, index: int):
        """
        Saves a byte sequence to dictionary at specified index.
        """
        self._matches[key] = index

    def get_match(self, key, index: int) -> Optional[int]:
        """
        Returns the index where key was last encountered in the original data.
        """
        found_index = self._matches.get(key, None)
        if found_index is not None and (found_index < index - self.SEARCH_LIMIT or found_index >= index):
            del self._matches[key]
            return None
        return found_index

    def get_byte(self, index: int) -> bytes:
        """
        Returns a byte from the original data at specified index.
        """
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

    def decode(self) -> bytes:
        """
        Performs the decoding of the input data.
        """
        data_in_bits = bitarray(endian='big')
        data_in_bits.frombytes(self._original_data)
        output_buffer = bytearray()
        index = 0
        while index < len(data_in_bits):
            bit_flag = data_in_bits[index]
            index += 1
            if bit_flag == 1:
                match_length = convert.bytes_to_char_int(
                    data_in_bits[index: index + _LENGTH_BITS].tobytes()) >> _LENGTH_BITS
                index += _LENGTH_BITS
                offset = convert.bytes_to_char_int(data_in_bits[index: index + _OFFSET_BITS].tobytes()) >> _LENGTH_BITS
                index += _OFFSET_BITS
                if match_length > 0:
                    for _ in range(match_length):
                        start = len(output_buffer) - offset
                        end = start + 1
                        bytes_to_write = bytes(output_buffer[start: end])
                        output_buffer.extend(bytes_to_write)
            if index + 8 <= len(data_in_bits):
                final_byte = data_in_bits[index: index + 8].tobytes()
                output_buffer.extend(final_byte)
            index += 8
        return bytes(output_buffer)
