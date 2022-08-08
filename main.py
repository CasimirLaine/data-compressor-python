import os
import sys
from pathlib import Path

root_path = Path(__file__).resolve().parent
path_prefix = f'{root_path}{os.sep}'
sys.path.append(f'{path_prefix}src')

from compress import lz, ui

if __name__ == '__main__':
    for file in os.scandir('temp'):
        os.remove(file.path)
    compressor = lz.LZEncode()
    original_text = 'testing' * 20000
    encoded = compressor.encode(data=original_text.encode()).decode(encoding='UTF-8', errors='replace')
    print(len(original_text))
    print(len(encoded))
    print(original_text)
    print(encoded)
    ui.EncoderProgram(sys.argv).start()
