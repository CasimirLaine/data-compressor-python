"""
Contains the Node class to use in a Huffman tree.
"""
import json
import string
from typing import Optional

from bitarray import bitarray


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
        """
        Converts the byte encoded in integer format to string.
        """
        try:
            symbol_chr = chr(self.symbol)
            if symbol_chr in string.ascii_letters or symbol_chr in string.digits:
                return symbol_chr
            return 'not printable'
        except Exception:
            return "null"
