import getopt
import sys


class _CommandLineArgument:

    def __init__(
            self,
            *
            short: str,
            long: str,
            hint: str,
    ):
        super().__init__()
        self.short = short
        self.long = long
        self.hint = hint


_OPTIONS = {

}


def start(arg_string):
    try:
        opts, args = getopt.getopt(arg_string, 'a:f:o:', ['algorithm=', 'file', 'output='])
    except getopt.GetoptError:
        _print_help()
        sys.exit(1)
    print(opts)
    print(args)


def _print_help():
    print(f'{__name__} -a <algorithm> -f <input_file> -o <output_file>')
