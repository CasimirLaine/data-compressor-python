"""
This module contains the base classes for the encoding algorithms.
"""
from typing import Type


class Encoder:
    """
    Class from which to inherit to implement an encoder.
    """

    def encode(self, data: bytes) -> bytes:
        """
        Override this method to encode data.
        """
        raise NotImplementedError


class Decoder:
    """
    Class from which to inherit to implement a decoder.
    """

    def decode(self, data: bytes) -> bytes:
        """
        Override this method to decode data.
        """
        raise NotImplementedError


class CompressionAlgorithm:
    """
    A class from which to inherit to implement compression algorithm.
    """

    @classmethod
    def get_encoder(cls) -> Type[Encoder]:
        """
        Returns the encoder as a type.
        """
        raise NotImplementedError

    @classmethod
    def get_decoder(cls) -> Type[Decoder]:
        """
        Returns the decoder as a type
        """
        raise NotImplementedError
