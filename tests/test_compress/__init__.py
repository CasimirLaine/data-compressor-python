import os
import sys
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parent.parent.parent
path_prefix = f'{ROOT_PATH}{os.sep}'
sys.path.append(f'{path_prefix}src')
