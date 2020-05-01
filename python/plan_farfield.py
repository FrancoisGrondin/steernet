import argparse
import json
import librosa as lr
import math
import numpy as np
import random as rnd
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--root', default='', type=str, help='Root folder with all audio files')
parser.add_argument('--json', default='', type=str, help='JSON with parameters')
args = parser.parse_args()

with open(args.json, 'r') as f:
	params = json.load(f)

for idx, path in enumerate(Path(args.root).rglob('*.%s' % params['extension']['audio'])):

	with open(path.with_suffix('.' + params['extension']['meta']), 'r') as f:
		meta = json.load(f)

	meta['snr'] = (np.round(np.random.uniform(params['snr']['min'], params['snr']['max'], len(meta['srcs'])) * 10) / 10).tolist()
	meta['gain'] = (np.round(np.random.uniform(params['gain']['min'], params['gain']['max'], len(meta['mics'])) * 100) / 100).tolist()
	meta['volume'] = round(rnd.uniform(params['volume']['min'], params['volume']['max']) * 100) / 100
	meta['path'] = str(path)

	print(json.dumps(meta))
