import os
import sys
from pathlib import Path

root_path = Path(__file__).resolve().parent
path_prefix = f'{root_path}{os.sep}'
sys.path.append(f'{path_prefix}src')

import lz

if __name__ == '__main__':
    compressor = lz.LZCompressor(
        search_buffer_size=16,
        lookahead_buffer_size=8
    )
    print(compressor.encode('test' * 100))
