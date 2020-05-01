
import argparse
import torch

from model.blstm import Blstm

parser = argparse.ArgumentParser()
parser.add_argument('--json', default='', type=str, help='JSON with parameters')
parser.add_argument('--model_dst', default='init.bin', type=str, help='Model to save')
args = parser.parse_args()

# Save

torch.save(Blstm(file_json=args.json).state_dict(), args.model_dst)
