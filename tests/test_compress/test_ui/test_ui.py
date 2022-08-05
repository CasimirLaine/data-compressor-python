import pytest

from compress import ui


def test_empty_input_file():
    with pytest.raises(RuntimeError):
        ui.EncoderProgram(['program.py'])


def test_help_string():
    strings_to_check = {'-', '--', '=', '<', '>',
                        ui.Commands.HELP,
                        ui.Commands.ALGORITHM,
                        ui.Commands.OUTPUT_FILE,
                        ui.Commands.FILE,
                        ui.Commands.METHOD,
                        }
    help_string = ui.help_string('program.py')
    for string in strings_to_check:
        assert string in help_string


def test_help_string_path():
    test_path = 'test/program.py'
    assert ui.help_string(test_path).startswith(test_path)
