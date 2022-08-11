# data-compressor-python

<b>Python</b> implementation of the <i>Lempel-Ziv</i> and <i>Huffman</i> compression algorithms.

## Problem

Reduce the size of files and text by compressing the data.

## Solution

Create a program that takes files and text as input, compresses the data with the Lempel-Ziv and Huffman compression algorithms and outputs the compressed data.

## Data Structures and Algorithms Used

LZ77 variation of the Lempel-Ziv compression algorithm.
Huffman encoding algorithm.

## Usage

The program has two methods: compress and decompress.
The program can receive text strings as file paths from input to the terminal.
File in that path will be compressed/decompressed and written to an output file.

## Performance goals

### Encoding: 

Time complexity: O(n)

Space complexity: O(n + m)

### Decoding: 

Time complexity: O(n)

Space complexity: O(n + m)

## Notes

Programming Language: Python

Degree Programme: Bachelor’s in Computer Science

Documentation & Implementation language: English

## Sources

https://en.wikipedia.org/wiki/LZ77_and_LZ78

https://www.cs.helsinki.fi/u/puglisi/dct2017

https://towardsdatascience.com/how-data-compression-works-exploring-lz77-3a2c2e06c097
