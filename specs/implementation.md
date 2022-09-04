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
| sample/lorem.txt        | 0.0140 | 0.0872 | 88.319 | 47.287 | 0.535 |
| sample/shakespeare.txt | 0.0022 | 0.0127 | 8.248 | 8.44 | 1.023 |
| sample/simple_image.png    | 0.3838 | 3.5421 | 2318.468 | 2317.23 | 0.999 |
| sample/small_image.jpeg        | 0.0006 | 0.0021 | 2.185 | 1.149 | 0.526 |
| n = 1 000               | 0.0004 | 0.0014 | 0.977 | 0.94 | 0.962 |
| n = 10 000              | 0.0017 | 0.0130 | 9.766 | 8.295 | 0.849 |
| n = 100 000             | 0.0154 | 0.1293 | 97.656 | 82.034 | 0.84 |
| n = 1 000 000           | 0.1539 | 1.3002 | 976.562 | 820.071 | 0.84 |
| n = 10 000 000          | 1.5294 | 13.0185 | 9765.625 | 8201.83 | 0.84 |
| n = 100 000 000         | 15.3192 | 131.7794 | 97656.25 | 82027.387 | 0.84 |

## Notes

.

## [Sources](sources.md)
