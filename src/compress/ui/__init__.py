import getopt

from compress.common import io, CompressionAlgorithm


class Commands:
    HELP = 'help'
    ALGORITHM = 'algorithm'
    OUTPUT_FILE = 'output_file'
    FILE = 'file'
    METHOD = 'method'


class Algorithm:
    LZ77 = 'lz77'
    HUFFMAN = 'huffman'


class Method:
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
    Algorithm.LZ77: CompressionAlgorithm,
    Algorithm.HUFFMAN: CompressionAlgorithm
}


class EncoderProgram:

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
        if Commands.HELP in self._options:
            print(help_string(self._program_path))
        data = self._get_data()
        compression_algorithm = self._get_compression_algorithm()
        method = self._get_method()
        if method == Method.DECODE:
            result = compression_algorithm.get_decoder()().decode(data)
        else:
            result = compression_algorithm.get_encoder()().encode(data)
        output_file_path = self._options.get(Commands.OUTPUT_FILE, f'{self._input_file}.encoded')
        io.write_file(output_file_path, result)

    def _get_data(self) -> bytes:
        return io.read_file(self._input_file)

    def _get_compression_algorithm(self) -> CompressionAlgorithm:
        compression_algorithm_name = self._options.get(Commands.ALGORITHM, Algorithm.LZ77)
        compression_algorithm = _ALGORITHMS.get(compression_algorithm_name, None)
        if compression_algorithm is None:
            compression_algorithm = _ALGORITHMS.get(Algorithm.LZ77)
        return compression_algorithm

    def _get_method(self):
        method = self._options.get(Commands.METHOD, None)
        if method != Method.ENCODE and method != Method.DECODE:
            method = Method.ENCODE
        return method


def _parse_args(arg_list: list[str]) -> tuple[list[tuple[str, str]], list[str]]:
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
    option_dict = {}
    for option in options:
        for command, arg in _OPTIONS.items():
            if option[0] == f'-{arg.short.rstrip(":")}' or option[0] == f'--{arg.long.rstrip("=")}':
                option_dict[command] = option[1]
    return option_dict


def help_string(program_path: str):
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
