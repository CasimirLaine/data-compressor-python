from typing import Type


class Encoder:
    def encode(self, data: bytes) -> bytes:
        raise NotImplementedError


class Decoder:

    def decode(self, data: bytes) -> bytes:
        raise NotImplementedError


class CompressionAlgorithm:
    @classmethod
    def get_encoder(cls) -> Type[Encoder]:
        raise NotImplementedError

    @classmethod
    def get_decoder(cls) -> Type[Decoder]:
        raise NotImplementedError
