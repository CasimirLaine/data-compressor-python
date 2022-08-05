import os
import sys
from pathlib import Path

root_path = Path(__file__).resolve().parent
path_prefix = f'{root_path}{os.sep}'
sys.path.append(f'{path_prefix}src')

from compress import lz

if __name__ == '__main__':
    compressor = lz.LZCompressor()
    original_text = 'testing' * 20000
    encoded = compressor.encode(original_text)
    print(len(original_text))
    print(len(encoded))
    print(original_text)
    print(encoded)
