import bisect
import sys
from typing import Type, Optional

from bitarray import bitarray

from compress.common import Encoder, Decoder, CompressionAlgorithm, convert


class Node:
    def __init__(
            self,
            *,
            probability: int,
            symbol: Optional[int] = None,
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
        decoder = _HuffmanDecodingProcess(self, data)
        return decoder.decode()


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

    def get_header_info(self, buffer: bitarray, node: Node):
        if node.left:
            self.get_header_info(buffer, node.left)
        if node.right:
            self.get_header_info(buffer, node.right)
        if node.left is node.right is None:
            buffer.append(1)
            buffer.frombytes(node.symbol.to_bytes(length=1, byteorder=sys.byteorder))
            print(node.symbol.to_bytes(length=1, byteorder=sys.byteorder))
        else:
            buffer.append(0)
        buffer.append(0)

    def encode(self) -> bytes:
        root_node = self.construct_tree()
        codes = {}
        self.update_codes(root_node, '', codes)
        header_buffer = bitarray()
        self.get_header_info(header_buffer, root_node)
        output_buffer = bitarray()
        for char in self._original_data:
            sequence = codes[char]
            output_buffer.extend(sequence)
        output_buffer.fill()
        output_data_bytes = bytes(output_buffer)
        return convert.int_to_bytes(
            len(output_data_bytes)
        ) + convert.int_to_bytes(
            len(codes)
        ) + convert.int_to_bytes(
            len(self._original_data)
        ) + bytes(header_buffer) + output_data_bytes


class _HuffmanDecodingProcess:

    def __init__(self, decoder: HuffmanDecoder, data: bytes):
        self._decoder = decoder
        self._original_data = data
        self._compressed_chars = convert.bytes_to_int(data[0:4])
        self._header_chars = convert.bytes_to_int(data[4:8])
        self._original_chars = convert.bytes_to_int(data[8:12])

    def decode(self) -> bytes:
        input_buffer = bitarray()
        input_buffer.frombytes(self._original_data[12:])
        output_buffer = bitarray()
        index = 0
        char_stack = []
        while index < len(input_buffer):
            bit = input_buffer[index]
            if bit == 0:
                # if len(char_stack) == 1:
                print(char_stack)
                index += 1
            elif bit == 1:
                index += 1
                character = input_buffer[index: index + 8].tobytes()
                char_stack.append(character)
                index += 8
        return bytes(output_buffer)
