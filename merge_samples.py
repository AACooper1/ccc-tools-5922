#!/usr/bin/env python3

import json
from pathlib import Path

from defines import Language


CODE_DIR = Path('code_blocks')
NONCODE_DIR = Path('luna_sample')
SAMPLES_DIR = Path('samples')


SAMPLES_DIR.mkdir(exist_ok=True)

for language in Language:
    with (
            open(CODE_DIR / Path(f'{language}.json'), 'r') as code_file,
            open(NONCODE_DIR / Path(f'{language}.json'), 'r') as noncode_file,
            open(SAMPLES_DIR / Path(f'{language}.json'), 'w') as sample_file,
    ):
        code_data = json.load(code_file)
        noncode_data = json.load(noncode_file)
        json.dump(code_data + noncode_data, sample_file)
