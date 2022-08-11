import bisect
from typing import Type

from bitarray import bitarray

from compress.common import Encoder, Decoder, CompressionAlgorithm


class Node:
    def __init__(
            self,
            *,
            probability: int,
            symbol: int,
            left: 'Node' = None,
            right: 'Node' = None
    ) -> None:
        self.probability = probability
        self.symbol = symbol
        self.left = left
        self.right = right
        self.code: bitarray = bitarray()


class HuffmanEncoder(Encoder):
    def encode(self, data: bytes) -> bytes:
        encoding_process = _HuffmanEncodingProcess(self, data)
        return encoding_process.encode()


class HuffmanDecoder(Decoder):
    def decode(self, data: bytes) -> bytes:
        return data


class Huffman(CompressionAlgorithm):

    @classmethod
    def get_encoder(cls) -> Type[Encoder]:
        return HuffmanEncoder

    @classmethod
    def get_decoder(cls) -> Type[Decoder]:
        return HuffmanDecoder


class _HuffmanEncodingProcess:
    """
    Protected class to maintain the internal state of a single compression run.
    """

    def __init__(self, compressor: HuffmanEncoder, data: bytes):
        self._compressor = compressor
        self._original_data = data

    def calculate_probabilities(self) -> dict[int, int]:
        probabilities = {}
        for char in self._original_data:
            if char in probabilities:
                probabilities[char] += 1
            else:
                probabilities[char] = 1
        return probabilities

    def construct_tree(self) -> Node:
        probabilities = self.calculate_probabilities()
        nodes: list[Node] = []
        sort_func = lambda node: -1 * node.probability
        for symbol, probability in probabilities.items():
            bisect.insort_right(a=nodes, x=Node(probability=probability, symbol=symbol), key=sort_func)
        while len(nodes) > 1:
            left = nodes.pop(-1)
            right = nodes.pop(-1)
            left.code.append(0)
            right.code.append(1)
            combined = Node(
                probability=left.probability + right.probability,
                symbol=left.symbol + right.symbol,
                left=left,
                right=right
            )
            bisect.insort_right(a=nodes, x=combined, key=sort_func)
        return nodes[0]

    def update_codes(self, node: Node, code, codes: dict):
        new_code = code + node.code.to01()
        if node.left:
            self.update_codes(node.left, new_code, codes)
        if node.right:
            self.update_codes(node.right, new_code, codes)
        if node.left is node.right is None:
            codes[node.symbol] = new_code

    def encode(self) -> bytes:
        root_node = self.construct_tree()
        codes = {}
        self.update_codes(root_node, '', codes)
        output_buffer = bitarray()
        for char in self._original_data:
            sequence = codes[char]
            output_buffer.extend(sequence)
        output_buffer.fill()
        return bytes(output_buffer)
