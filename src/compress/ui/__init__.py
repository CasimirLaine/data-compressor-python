"""
This module is responsible for rendering the command line interface.
"""
import getopt
import sys

from compress.common import io, CompressionAlgorithm
from compress.lz import LZ


class Commands:
    """
    Contains all the commands the user can feed into the program.
    """
    HELP = 'help'
    ALGORITHM = 'algorithm'
    OUTPUT_FILE = 'output_file'
    FILE = 'file'
    METHOD = 'method'


class Algorithm:
    """
    Contains all the algorithms the user can choose from.
    """
    LZ77 = 'lz77'
    HUFFMAN = 'huffman'


class Method:
    """
    Contains all the methods that can be performed on input data.
    """
    ENCODE = 'encode'
    DECODE = 'decode'


class _CommandLineArgument:

    def __init__(
            self,
            *,
            short: str,
            long: str,
            hint: str = None,
    ):
        super().__init__()
        self.short = short
        self.long = long
        self.hint = hint


_OPTIONS: dict[str, _CommandLineArgument] = {
    Commands.HELP: _CommandLineArgument(short='h', long='help'),
    Commands.ALGORITHM: _CommandLineArgument(short='a:', long='algorithm=', hint='algorithm'),
    Commands.OUTPUT_FILE: _CommandLineArgument(short='o:', long='output_file=', hint='output_file'),
    Commands.FILE: _CommandLineArgument(short='f:', long='file=', hint='file'),
    Commands.METHOD: _CommandLineArgument(short='m:', long='method=', hint='method'),
}

_ALGORITHMS: dict[str, CompressionAlgorithm] = {
    Algorithm.LZ77: LZ,
    Algorithm.HUFFMAN: CompressionAlgorithm
}


class EncoderProgram:
    """
    Class used to initialize the command line interface.
    It will process command line arguments and interpret them as commands.
    """

    def __init__(self, arg_list: list[str]):
        super().__init__()
        options, args = _parse_args(arg_list)
        self._options = _compose_options_dict(options)
        self._program_path = arg_list[0]
        self._arg_list = arg_list[1:]
        self._input_file = self._options.get(Commands.FILE, None)
        if not self._input_file:
            print(help_string(self._program_path))
            raise RuntimeError

    def start(self):
        """
        This method is used to start the process that the user chose with command line arguments.
        """
        if Commands.HELP in self._options:
            print(help_string(self._program_path))
        data = self._get_data()
        compression_algorithm = self._get_compression_algorithm()
        method = self._get_method()
        if method == Method.DECODE:
            result = compression_algorithm.get_decoder()().decode(data)
        else:
            result = compression_algorithm.get_encoder()().encode(data)
        output_file_path = self._options.get(Commands.OUTPUT_FILE, f'{self._input_file}.output')
        try:
            io.write_file(output_file_path, result)
        except FileExistsError:
            print(f'File {output_file_path} already exists')
            sys.exit(-1)
        except IOError:
            print(f'Could not write to file {output_file_path}')
            sys.exit(-1)

    def _get_data(self) -> bytes:
        """
        Read the entire file the user provided as an input.
        """
        try:
            return io.read_file(self._input_file)
        except IOError:
            print(f'Could not read file {self._input_file}')
            sys.exit(-1)

    def _get_compression_algorithm(self) -> CompressionAlgorithm:
        """
        Returns the type of compression algorithm the user chose.
        """
        compression_algorithm_name = self._options.get(Commands.ALGORITHM, Algorithm.LZ77)
        compression_algorithm = _ALGORITHMS.get(compression_algorithm_name, None)
        if compression_algorithm is None:
            compression_algorithm = _ALGORITHMS.get(Algorithm.LZ77)
        return compression_algorithm

    def _get_method(self):
        """
        Returns the method the user chose for processsing the input.
        """
        method = self._options.get(Commands.METHOD, None)
        if method != Method.ENCODE and method != Method.DECODE:
            method = Method.ENCODE
        return method


def _parse_args(arg_list: list[str]) -> tuple[list[tuple[str, str]], list[str]]:
    """
    Parses the command line argument while conforming to the GNU CLI standards.
    """
    if len(arg_list) < 1:
        print(help_string(arg_list[0]))
        raise RuntimeError
    shorts = ''
    longs = []
    for command_line_arg in _OPTIONS.values():
        shorts += command_line_arg.short
        longs.append(command_line_arg.long)
    try:
        opts, args = getopt.getopt(arg_list[1:], shorts, longs)
    except getopt.GetoptError:
        print(help_string(arg_list[0]))
        raise
    return opts, args


def _compose_options_dict(options):
    """
    Transforms the command line arguments into a more readable format.
    """
    option_dict = {}
    for option in options:
        for command, arg in _OPTIONS.items():
            if option[0] == f'-{arg.short.rstrip(":")}' or option[0] == f'--{arg.long.rstrip("=")}':
                option_dict[command] = option[1]
    return option_dict


def help_string(program_path: str):
    """
    Returns the help string of the program.
    Used then -h or --help is present in the command line arguments.
    Also printed when a misuse of the program is detected.
    """
    output_string = program_path
    for command_line_arg in _OPTIONS.values():
        output_string += f' -{command_line_arg.short.rstrip(":")}'
        if ':' in command_line_arg.short:
            output_string += f' <{command_line_arg.hint}>'
        output_string += f' --{command_line_arg.long.rstrip("=")}'
        if '=' in command_line_arg.long:
            output_string += f'=<{command_line_arg.hint}>'
    output_string += ' <input>'
    return output_string
