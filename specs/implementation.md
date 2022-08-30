# Implementation

## Structure

## Complexity

### Lempel-Ziv

#### Encoding:

#### Decoding:

### Huffman

#### Encoding:

#### Decoding:

## Performance Results

### Lempel-Ziv

#### Encoding:

#### Decoding:

### Huffman

| Sample                  | Encoding Speed (s) | Decoding Speed (s) | Original Data (KB) | Compressed Data (KB) | Compression Ratio (%) |
|-------------------------|---|---|---|---|---|
| sample/simple.txt       | 0.0001 | 0.0001 | 0.078 | 0.048 | 0.615 |
| sample/lorem.txt        | 0.0140 | 0.0872 | 88.319 | 47.287 | 0.535 |
| sample/small_image.jpeg | 0.0022 | 0.0127 | 8.248 | 8.44 | 1.023 |
| sample/big_image.jpg    | 0.3838 | 3.5421 | 2318.468 | 2317.23 | 0.999 |
| sample/image.png        | 0.0006 | 0.0021 | 2.185 | 1.149 | 0.526 |
| n = 1 000               | 0.0004 | 0.0014 | 0.977 | 0.94 | 0.962 |
| n = 10 000              | 0.0017 | 0.0130 | 9.766 | 8.295 | 0.849 |
| n = 100 000             | 0.0154 | 0.1293 | 97.656 | 82.034 | 0.84 |
| n = 1 000 000           | 0.1539 | 1.3002 | 976.562 | 820.071 | 0.84 |
| n = 10 000 000          | 1.5294 | 13.0185 | 9765.625 | 8201.83 | 0.84 |
| n = 100 000 000         | 15.3192 | 131.7794 | 97656.25 | 82027.387 | 0.84 |

## Notes

.

## [Sources](sources.md)
