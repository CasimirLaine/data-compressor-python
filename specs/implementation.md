# Implementation

## Structure

### Lempel-Ziv

The data is encoded into sequences of three bytes.
The first 4 bits are the offset left of the current position.
The next 12 bits represent the length of the match.
The remaining byte is the next byte in the original data.

However, an optimization is made when the match length is under 3 bytes.
In that case only the byte is inserted.

To decode this variable-width data 0 bit is inserted before the three bytes when match is found.
If only the byte is written a 1 bit is inserted before the byte.

### Huffman

In the beginning of the data there is a header of three 32-bit integers.
These are:
- Size of the Huffman tree in bytes.
- Amount of unique bytes in the original data.
- Size of the original data in bytes.

The Huffman tree is stored after the header.
This tree is encoded with post-order traversal, starting from the left.
When a leaf node is encountered 1 bit is appended after which the byte that the leaf node represents is inserted.
Other nodes in the tree will output 0 bit in the encoding.

After the Huffman tree the data encoded according to the tree is written.

## Complexity

### Lempel-Ziv

#### Encoding:

The encoding algorithm approaches linear time since the input is processed in a single loop.
Inside that loop, however, some matches are found recursively.
This recursion still has a stack limit of 15 since the length of the match cannot be longer.
This is due to the limit of four bits that are allocated for the match length in the output.
Further, the matches of the already-processed part of the input are store in a dict.
Dict has a O(1) constant time complexity in access operations.
So accessing past matches will not affect time complexity.

Time complexity: O(n).

#### Decoding:

Much like the encoding, the decoder processed the input in a single while-loop.
Looping over the data and appending matches to an output buffer.

Time complexity: O(n).

### Huffman

#### Encoding:

#### Decoding:

## Performance Results

### Lempel-Ziv

| Sample                  | Encoding Speed (s) | Decoding Speed (s) | Original Data (KB) | Compressed Data (KB) | Compression Ratio |
|-------------------------|---|---|---|---|---|
| sample/simple.txt       | 0.0001 | 0.0000 | 0.078 | 0.065 | 0.833 |
| sample/lorem.txt        | 0.0955 | 0.0266 | 88.319 | 58.291 | 0.66 |
| sample/shakespeare.txt | 6.4050 | 1.6093 | 5330.272 | 3901.245 | 0.732 |
| sample/simple_image.png    | 0.0020 | 0.0005 | 2.185 | 0.878 | 0.402 |
| sample/small_image.jpeg        | 0.0129 | 0.0020 | 8.248 | 9.026 | 1.094 |
| n = 1 000               | 0.0014 | 0.0002 | 0.977 | 1.099 | 1.125 |
| n = 10 000              | 0.0173 | 0.0024 | 9.766 | 10.978 | 1.124 |
| n = 100 000             | 0.1893 | 0.0238 | 97.656 | 109.718 | 1.124 |
| n = 1 000 000           | 1.9506 | 0.2337 | 976.562 | 1096.839 | 1.123 |
| n = 10 000 000          | 21.3077 | 2.3422 | 9765.625 | 10968.202 | 1.123 |
| n = 100 000 000         | 233.3153 | 23.7175 | 97656.25 | 109682.097 | 1.123 |

### Huffman

| Sample                  | Encoding Speed (s) | Decoding Speed (s) | Original Data (KB) | Compressed Data (KB) | Compression Ratio |
|-------------------------|---|---|---|---|---|
| sample/simple.txt       | 0.0001 | 0.0001 | 0.078 | 0.048 | 0.615 |
| sample/lorem.txt        | 0.0126 | 0.0855 | 88.319 | 47.287 | 0.535 |
| sample/shakespeare.txt | 0.7357 | 5.4583 | 5330.272 | 3083.375 | 0.578 |
| sample/simple_image.png    | 0.0006 | 0.0021 | 2.185 | 1.149 | 0.526 |
| sample/small_image.jpeg        | 0.0022 | 0.0138 | 8.248 | 8.44 | 1.023 |
| n = 1 000               | 0.0004 | 0.0014 | 0.977 | 0.938 | 0.96 |
| n = 10 000              | 0.0017 | 0.0129 | 9.766 | 8.296 | 0.849 |
| n = 100 000             | 0.0153 | 0.1281 | 97.656 | 82.016 | 0.84 |
| n = 1 000 000           | 0.1528 | 1.2804 | 976.562 | 820.079 | 0.84 |
| n = 10 000 000          | 1.5420 | 12.9038 | 9765.625 | 8201.985 | 0.84 |
| n = 100 000 000         | 15.3825 | 128.9075 | 97656.25 | 82027.189 | 0.84 |

## Notes

The LZ implementation does not seem to play well with totally random bytes.
The speed of LZ compression could be improved.

## [Sources](sources.md)
