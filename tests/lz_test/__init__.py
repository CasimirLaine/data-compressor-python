import os
import sys
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent.parent
path_prefix = f'{root_path}{os.sep}'
sys.path.append(f'{path_prefix}src')
