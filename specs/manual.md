# Manual

## Installation

- Download and install [Python version 3.10](https://www.python.org/downloads/) or newer.
- Clone this repository on your computer

## Running

To run the program:

```bash 
python main.py -h --help -a <algorithm> --algorithm=<algorithm> -o <output_file> --output_file=<output_file> -f <file> --file=<file> -m <method> --method=<method> <input>
```

### CLI Arguments

-h, --help

Prints the help string.

-a --algorithm

Selects the algorithm used.
Options: lz77, huffman, lzh, hlz

-o --output_file

Path of the file to create as an output.
By default, the input file gets ".output" appended to it.

-f --file

The file to either encode or decode.
Given as a full file path.

-m --method

The method to perform on the input file.
Options: encode, decode

## Samples

The project contains some sample file with which to test the program.
The sample files are located in [sample](https://github.com/CasimirLaine/data-compressor-python/tree/master/sample) folder.
