import os
import sys
from pathlib import Path

root_path = Path(__file__).resolve().parent
path_prefix = f'{root_path}{os.sep}'
sys.path.append(f'{path_prefix}src')

import lz

if __name__ == '__main__':
    compressor = lz.LZCompressor(
        search_buffer_size=16 * 100,
        lookahead_buffer_size=8 * 100
    )
    original_text = 'huiadhspvuapfhasdupifahdusi' * 10
    encoded = compressor.encode(original_text)
    print(len(original_text))
    print(len(encoded))
    print(original_text)
    print(encoded)

