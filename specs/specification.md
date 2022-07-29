# lempel-ziv-python

<b>Python</b> implementation of the <i>Lempel-Ziv</i> compression algorithm.

## Problem

Reduce the size of files and text by compressing the data.

## Solution

Create a program that takes files and text as input, compresses the data with Lempel-Ziv compression algorithm and output the compressed data.

## Data Structures and Algorithms Used

LZ77 variation of the Lempel-Ziv compression algorithm.

## Usage

The program has two methods: compress and decompress.
The program can receive text strings and file paths as input to the terminal.
Text strings will be compressed/decompressed and printed.
File path input will compress/decompress the file provided by the path into a new file.

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
