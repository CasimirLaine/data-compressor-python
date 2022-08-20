"""
This module is used as an API for developers to encode and decode data with the Huffman algorithm.
"""
import bisect
import json
import string
from typing import Type, Optional

from bitarray import bitarray

from compress.common import Encoder, Decoder, CompressionAlgorithm, convert


class Node:
    """
    Represents a node in the Huffman tree.
    """

    def __init__(
            self,
            *,
            probability: int = 0,
            symbol: Optional[int] = None,
            left: 'Node' = None,
            right: 'Node' = None
    ) -> None:
        self.probability = probability
        self.symbol = symbol
        self.left = left
        self.right = right
        self.code: bitarray = bitarray()

    def __repr__(self) -> str:
        output_str = '{\n'
        if self.left:
            output_str += f'"left": {self.left},\n'
        if self.right:
            output_str += f'"right": {self.right},\n'
        output_str += f'"probability": "{self.probability}",\n'
        output_str += f'"symbol": "{self.symbol}",\n'
        output_str += f'"char": "{self.symbol_to_char}",\n'
        output_str += f'"code": "{self.code}"\n'
        output_str += '}'
        return json.dumps(json.loads(output_str), indent=2)

    @property
    def symbol_to_char(self):
        try:
            symbol_chr = chr(self.symbol)
            if symbol_chr in string.ascii_letters or symbol_chr in string.digits:
                return symbol_chr
            return 'not printable'
        except Exception:
            return "null"


def sort_func_node(node: Node):
    return -1 * node.probability


class HuffmanEncoder(Encoder):
    """
    Used to encode data with the Huffman algorithm.
    """

    def encode(self, data: bytes) -> bytes:
        encoding_process = _HuffmanEncodingProcess(self, data)
        return encoding_process.encode()


class HuffmanDecoder(Decoder):
    """
    Used to decode data with the Huffman algorithm.
    """

    def decode(self, data: bytes) -> bytes:
        decoder = _HuffmanDecodingProcess(self, data)
        return decoder.decode()


class Huffman(CompressionAlgorithm):
    """
    Links the Encoder and Decoder implementing the Huffman algorithm.
    """

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
        for symbol, probability in probabilities.items():
            bisect.insort_right(a=nodes, x=Node(probability=probability, symbol=symbol), key=sort_func_node)
        while len(nodes) > 1:
            left = nodes.pop()
            right = nodes.pop()
            left.code.append(0)
            right.code.append(1)
            combined = Node(
                probability=left.probability + right.probability,
                left=left,
                right=right
            )
            bisect.insort_right(a=nodes, x=combined, key=sort_func_node)
        return nodes[0]

    def update_codes(self, node: Node, code: str, codes: dict):
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
            buffer.frombytes(convert.char_int_to_bytes(node.symbol))
        else:
            buffer.append(0)

    def encode(self) -> bytes:
        root_node = self.construct_tree()
        codes = {}
        self.update_codes(root_node, '', codes)
        header_buffer = bitarray()
        self.get_header_info(header_buffer, root_node)
        header_buffer.fill()
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
    """
    Protected class to maintain the internal state of a single decompression run.
    """

    def __init__(self, decoder: HuffmanDecoder, data: bytes):
        self._decoder = decoder
        self._original_data = data
        self._compressed_chars = convert.bytes_to_int(data[0:4])
        self._header_chars = convert.bytes_to_int(data[4:8])
        self._original_chars = convert.bytes_to_int(data[8:12])

    def decode_header(self, input_buffer: bitarray):
        index = 0
        node_stack = []
        node_count = 0

        def merge():
            right = node_stack.pop()
            left = node_stack.pop()
            node = Node(left=left, right=right)
            node_stack.append(node)

        while index < len(input_buffer) and node_count < self._header_chars:
            bit = input_buffer[index]
            if bit == 0:
                if len(node_stack) > 1:
                    merge()
                index += 1
            elif bit == 1:
                index += 1
                character = input_buffer[index: index + 8]
                node_stack.append(Node(symbol=convert.bytes_to_char_int(character.tobytes())))
                index += 8
                node_count += 1
        while len(node_stack) > 1:
            merge()
        index += (8 - index % 8)
        return node_stack.pop(), index

    def find_char(self, node: Node, input_buffer: bitarray, index: int):
        if node.left is node.right is None:
            return node.symbol, index
        bit_found = input_buffer[index]
        if bit_found == 0:
            return self.find_char(node.left, input_buffer, index + 1)
        elif bit_found == 1:
            return self.find_char(node.right, input_buffer, index + 1)

    def decode(self) -> bytes:
        input_buffer = bitarray()
        input_buffer.frombytes(self._original_data[12:])
        output_buffer = bitarray()
        root_node, index = self.decode_header(input_buffer)
        char_count = 0
        while index < len(input_buffer) and char_count < self._original_chars:
            char_found, index = self.find_char(root_node, input_buffer, index)
            char_count += 1
            output_buffer.frombytes(convert.char_int_to_bytes(char_found))
        return bytes(output_buffer)
