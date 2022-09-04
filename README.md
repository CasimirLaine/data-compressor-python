# data-compressor-python

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![PyCharm](https://img.shields.io/badge/pycharm-143?style=for-the-badge&logo=pycharm&logoColor=black&color=black&labelColor=green)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)
[![Pylint](https://github.com/CasimirLaine/data-compressor-python/actions/workflows/pylint.yml/badge.svg?branch=master)](https://github.com/CasimirLaine/data-compressor-python/actions/workflows/pylint.yml)
[![pages-build-deployment](https://github.com/CasimirLaine/data-compressor-python/actions/workflows/pages/pages-build-deployment/badge.svg?branch=master)](https://github.com/CasimirLaine/data-compressor-python/actions/workflows/pages/pages-build-deployment)

<b>Python</b> implementation of the <i>Lempel-Ziv</i> and <i>Huffman</i> compression algorithms.

## Documentation

- [Project Specification](./specs/specification.md)
- [Implementation Document](./specs/implementation.md)
- [User Manual](./specs/manual.md)
- [Test Document](./specs/testing.md)
- [Weekly Reports](./specs/weekly)

This project supports Python version 3.10+!

## First steps

Build and fetch dependencies:

```bash
python setup.py
```

## Run configurations

### Run

To run the program:

```bash 
python main.py -h --help -a <algorithm> --algorithm=<algorithm> -o <output_file> --output_file=<output_file> -f <file> --file=<file> -m <method> --method=<method> <input>
```

Refer to the [user manual](./specs/testing.md) for more info.

### Performance Benchmarks

To run performance benchmarks:

```bash 
python performance.py
```

### Static Analysis

To run static code analysis tool (pylint):

```bash
pylint src
```

### Testing

To run unit tests:

```bash
pytest
```

To run unit tests in parallel:

```bash
pytest -n auto
```

### Generate Test Coverage

To generate and view test coverage:

```bash
pytest
open docs/index.html
```

On <b>Windows</b>:

```bash
pytest
start docs/index.html
```
