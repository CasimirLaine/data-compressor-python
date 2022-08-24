# Test Document

The program has been tested with **Python** version 3.10.

Program has been tested using various methods.
- Unit tests with pytest-module.
- Integration tests have been performed on different operating systems (Windows, Linux and macOS)
- Performance tests using timing.
- End-to-end tests by testing the application behaviour from the point-of-view of the user.

## Unit tests

### Application logic

The application logic has been tested via pytest test framework. Tests can be found in [tests](https://github.com/CasimirLaine/data-compressor-python/tree/master/tests) folder.

### Test coverage

The latest coverage report can be found [here](https://casimirlaine.github.io/data-compressor-python/).

### Testing

To run unit tests run the following command from the root of the project:

```bash
pytest
```

## Integration tests

Application has been tested in the following formats:

- Pycharm (Windows, Linux, macOS)
- Command line (Windows, Linux, macOS)

## Performance tests

Application's performance has been tested via the profiler integrated to Pycharm integrated development environment.
CPU and memory usage of the application are OK. No memory leaks detected.
IO-operations were also tested.
The application does not make network requests.

## End-to-end tests

The application has been tested according to the manual provided in the [user manual](./manual.md).
