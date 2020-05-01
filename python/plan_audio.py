
import argparse
import json
import random as rnd

parser = argparse.ArgumentParser()
parser.add_argument('--speech', default='', type=str, help='Meta for speech')
parser.add_argument('--farfield', default='', type=str, help='Meta for farfield')
parser.add_argument('--count', default=1, type=int, help='Number of audio samples')
args = parser.parse_args()

with open(args.farfield) as f:
	farfield_elements = f.read().splitlines()

with open(args.speech) as f:
	speech_elements = f.read().splitlines()

for i in range(0, args.count):

	meta = {}

	meta['farfield'] = json.loads(rnd.choice(farfield_elements))

	meta['speech'] = []
	speech_jsons = rnd.choices(speech_elements, k=len(meta['farfield']['srcs']))
	for speech_json in speech_jsons:
		meta['speech'].append(json.loads(speech_json))

	print(json.dumps(meta))

