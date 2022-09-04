"""
This module is used as an API for developers to encode and decode data with the Lempel-Ziv-Huffman algorithm.
"""
from typing import Type

from compress.common import CompressionAlgorithm, Decoder, Encoder
from compress.huffman import HuffmanEncoder, HuffmanDecoder
from compress.lz import LZEncoder, LZDecoder


class LZHEncoder(Encoder):
    """
    Functions as the API for compression process.
    Uses the Lempel-Ziv-Huffman encoding algorithm to compress data.
    """

    def encode(self, data: bytes) -> bytes:
        """
        Function to call to provide input for the compressor to compress.
        Returns the compressed bytes.
        """
        lz_encoded = LZEncoder().encode(data)
        huffman_encoded = HuffmanEncoder().encode(lz_encoded)
        return huffman_encoded


class LZHDecoder(Decoder):
    """
    Functions as the API for decompression process.
    Uses the Lempel-Ziv-Huffman encoding algorithm to decompress data.
    """

    def decode(self, data: bytes) -> bytes:
        lz_encoded = HuffmanDecoder().decode(data)
        decoded = LZDecoder().decode(lz_encoded)
        return decoded


class LZH(CompressionAlgorithm):
    """
    Functions as the API for compression process.
    """

    @classmethod
    def get_encoder(cls) -> Type[Encoder]:
        return LZHEncoder

    @classmethod
    def get_decoder(cls) -> Type[Decoder]:
        return LZHDecoder
