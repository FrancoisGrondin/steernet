import argparse
import beam
import librosa as lr
import numpy as np
import torch
from scipy.io.wavfile import write

from dataset.array import Array
from model.blstm import Blstm

import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('--audio', default='', type=str, help='Meta for audio')
parser.add_argument('--json', default='', type=str, help='JSON of parameters')
parser.add_argument('--model_src', default='', type=str, help='Model to start training from')
parser.add_argument('--wave_dst', default='', type=str, help='Wave file to save result')
parser.add_argument('--index', default=0, type=int, help='Index of element in dataset')
args = parser.parse_args()

# Dataset

dataset = Array(file_meta=args.audio, file_json=args.json)

# Model

net = Blstm(file_json=args.json)
net.load_state_dict(torch.load(args.model_src))

# Evaluate

Xs, Ns, Ys, YYs = dataset[args.index]

M = beam.mask(YYs, net);
TTs, IIs = beam.cov(Ys, M)
Zs = beam.gev(Ys, TTs, IIs)
Cs = Xs[0,0,:,:]

XsTarget = np.transpose(Cs)
XsMixed = np.transpose(Ys[0,:,:])
XsGev = np.transpose(Zs)

xsTarget = np.expand_dims(lr.core.istft(XsTarget), 1)
xsMixed = np.expand_dims(lr.core.istft(XsMixed), 1)
xsGev = np.expand_dims(lr.core.istft(XsGev), 1)

xs = np.concatenate((xsTarget, xsMixed, xsGev), axis=1)

write(args.wave_dst, 16000, xs)
