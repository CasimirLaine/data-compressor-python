# Specification

<b>Python</b> implementation of the <i>Lempel-Ziv</i> and <i>Huffman</i> compression algorithms.

## Problem

Reduce the size of files and text by compressing the data.

## Solution

<!-- include(implementation.md) -->

Create a program that takes files as input, compresses the data with the Lempel-Ziv and Huffman compression algorithms
and outputs the compressed data.

## Data Structures and Algorithms Used

LZ77 variation of the Lempel-Ziv compression algorithm.
Huffman encoding algorithm.
For Huffman a tree data structure is implemented.

## Usage

The program has two methods: compress and decompress.
The program can receive text strings as file paths from input to the terminal.
File in that path will be compressed/decompressed and written to an output file.

## Performance Goals

### Lempel-Ziv

#### Encoding:

Time complexity: O(n)

Space complexity: O(n + m)

#### Decoding:

Time complexity: O(n)

Space complexity: O(n + m)

### Huffman

#### Encoding:

Time complexity: O(n log n)

Space complexity: O(n log n)

#### Decoding:

Time complexity: O(n log n)

Space complexity: O(n log n)

## Notes

Programming Language: Python

Degree Programme: Bachelor’s in Computer Science

Documentation & Implementation language: English

## [Sources](sources.md)
