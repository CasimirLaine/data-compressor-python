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
- [Test Document](https://casimirlaine.github.io/data-compressor-python/)
- [Weekly Reports](./specs/weekly)

## First steps

Build and fetch dependencies:

```bash
python setup.py
```

## Run configurations

### Run

To run the program:

```bash
python main.py
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

### Generate documentation

To generate and view API documentation:

```bash
```
