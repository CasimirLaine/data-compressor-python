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


def test_cli_args():
    options_dict = ui.compose_options_dict([
        (
            '-a', ui.Algorithm.LZ77
        ),
        (
            '-o', 'file.output'
        ),
        (
            '-f', 'file.txt'
        ),
        (
            '-m', ui.Method.ENCODE
        ),
        (
            '-h', None
        )
    ])
    assert options_dict[ui.Commands.ALGORITHM] == ui.Algorithm.LZ77
    assert options_dict[ui.Commands.OUTPUT_FILE] == 'file.output'
    assert options_dict[ui.Commands.FILE] == 'file.txt'
    assert options_dict[ui.Commands.METHOD] == ui.Method.ENCODE
    assert options_dict[ui.Commands.HELP] is None


def test_too_few_cli_args():
    with pytest.raises(SystemExit):
        ui.EncoderProgram(['python.py'])


def test_no_input_file():
    with pytest.raises(SystemExit):
        ui.EncoderProgram(['python.py, -h'])
