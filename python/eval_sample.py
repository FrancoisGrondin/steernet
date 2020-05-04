import argparse
import numpy as np
import torch

from dataset.pair import Pair
from model.blstm import Blstm

import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('--audio', default='', type=str, help='Meta for audio')
parser.add_argument('--json', default='', type=str, help='JSON of parameters')
parser.add_argument('--model_src', default='', type=str, help='Model to start training from')
parser.add_argument('--index', default=0, type=int, help='Index of element in dataset')
parser.add_argument('--scratch_directory', default=None, type=str, help='Directory to store temporary files')
args = parser.parse_args()

# Dataset

dataset = Pair(file_meta=args.audio, file_json=args.json, dir_scratch=args.scratch_directory)

# Model

net = Blstm(file_json=args.json)
net.load_state_dict(torch.load(args.model_src))

# Evaluate

net.eval()

X, M = dataset[args.index]

Xt = torch.from_numpy(X).unsqueeze(0)
Mt = torch.from_numpy(M).unsqueeze(0)
Yt = net(Xt)

Y = np.squeeze(Yt.detach().numpy())

plt.subplot(311)
plt.imshow(np.flipud(np.transpose(np.squeeze(X[:,:,0]))), aspect='auto')
plt.subplot(312)
plt.imshow(np.flipud(np.transpose(np.squeeze(M))), aspect='auto')
plt.subplot(313)
plt.imshow(np.flipud(np.transpose(np.squeeze(Y))), aspect='auto')
plt.show()