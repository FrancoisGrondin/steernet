
from torch.utils.data import Dataset
from dataset.audio import Audio

import json
import librosa as lr
import numpy as np

import os.path

class Array(Dataset):

	def __init__(self, file_meta, file_json):

		self.audio = Audio(file_meta=file_meta)

		with open(file_json, 'r') as f:
			features = json.load(f)

		self.frameSize = features['frame_size']
		self.hopSize = features['hop_size']
		self.epsilon = features['epsilon']

	def __len__(self):

		return len(self.audio)

	def __getitem__(self, idx):

		xs, ns, tdoas = self.audio[idx]

		nSrcs = xs.shape[0]
		nMics = xs.shape[1]
		nSamples = xs.shape[2]

		Ns = []

		for iMic in range(0, nMics):

			Ns.append(np.expand_dims(np.transpose(lr.core.stft(ns[iMic,:], n_fft=self.frameSize, hop_length=self.hopSize)), axis=0))

		ys = ns

		for iSrc in range(0, nSrcs):

			ys += xs[iSrc,:,:]

		Ys = []

		for iMic in range(0, nMics):

			Ys.append(np.expand_dims(np.transpose(lr.core.stft(ys[iMic,:], n_fft=self.frameSize, hop_length=self.hopSize)), axis=0))

		YYs = []

		k = np.transpose(np.expand_dims(np.arange(0, self.frameSize/2+1), axis=1))
		f = np.transpose(np.ones((1, Ys[0].shape[0]), dtype=np.float32))

		for iMic1 in range(0, nMics):
			
			for iMic2 in range(iMic1+1, nMics):

				tau = tdoas[0,iMic1] - tdoas[0,iMic2]
				A = np.exp(-1j*2*np.pi*tau*k*f/self.frameSize)

				YY = A * Ys[iMic1] * np.conj(Ys[iMic2])

				YY2 = np.zeros((Ys[0].shape[0], Ys[0].shape[1], Ys[0].shape[2], 2), dtype=np.float32)

				YY2[:,:,:,0] = np.log(np.abs(YY)**2 + self.epsilon) - np.log(self.epsilon)
				YY2[:,:,:,1] = np.angle(YY)

				YYs.append(YY2)

		Ns = np.concatenate(Ns, axis=0)
		Ys = np.concatenate(Ys, axis=0)
		YYs = np.concatenate(YYs, axis=0)

		Xs = np.zeros((nSrcs,nMics,Ys.shape[1],Ys.shape[2]), dtype=np.complex64)

		for iSrc in range(0, nSrcs):

			for iMic in range(0, nMics):

				Xs[iSrc,iMic,:,:] = np.transpose(lr.core.stft(xs[iSrc,iMic,:], n_fft=self.frameSize, hop_length=self.hopSize))

		return Xs, Ns, Ys, YYs

