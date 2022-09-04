"""
This module is used as an API for developers to encode and decode data with the Huffman-Lempel-Ziv algorithm.
"""
from typing import Type

from compress.common import CompressionAlgorithm, Decoder, Encoder
from compress.huffman import HuffmanEncoder, HuffmanDecoder
from compress.lz import LZEncoder, LZDecoder


class HLZEncoder(Encoder):
    """
    Functions as the API for compression process.
    Uses the Huffman-Lempel-Ziv encoding algorithm to compress data.
    """

    def encode(self, data: bytes) -> bytes:
        """
        Function to call to provide input for the compressor to compress.
        Returns the compressed bytes.
        """
        huffman_encoded = HuffmanEncoder().encode(data)
        lz_encoded = LZEncoder().encode(huffman_encoded)
        return lz_encoded


class HLZDecoder(Decoder):
    """
    Functions as the API for decompression process.
    Uses the Huffman-Lempel-Ziv encoding algorithm to decompress data.
    """

    def decode(self, data: bytes) -> bytes:
        huffman_encoded = LZDecoder().decode(data)
        decoded = HuffmanDecoder().decode(huffman_encoded)
        return decoded


class HLZ(CompressionAlgorithm):
    """
    Functions as the API for compression process.
    """

    @classmethod
    def get_encoder(cls) -> Type[Encoder]:
        return HLZEncoder

    @classmethod
    def get_decoder(cls) -> Type[Decoder]:
        return HLZDecoder
