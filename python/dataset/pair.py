
from torch.utils.data import Dataset
from dataset.audio import Audio

import json
import librosa as lr
import numpy as np

import os.path

class Pair(Dataset):

	def __init__(self, file_meta, file_json, dir_scratch):

		self.audio = Audio(file_meta=file_meta)

		with open(file_json, 'r') as f:
			features = json.load(f)

		self.frameSize = features['frame_size']
		self.hopSize = features['hop_size']
		self.c = features['c']
		self.alpha = features['alpha']
		self.beta = features['beta']
		self.epsilon = features['epsilon']
		self.dir_scratch = dir_scratch

	def __len__(self):

		return len(self.audio)

	def __getitem__(self, idx):

		if self.dir_scratch is not None:

			file_scratch = '%s%08u.npz' % (self.dir_scratch, idx)

		else:

			file_scratch = ""

		if not os.path.exists(file_scratch):

			xs, ns, tdoas = self.audio[idx]

			nSrcs = xs.shape[0]
			nMics = 2

			y1 = ns[0,:]
			y2 = ns[1,:]
			T1 = 0.0
			T2 = 0.0
			I1 = np.abs(lr.core.stft(y1, n_fft=self.frameSize, hop_length=self.hopSize))**2
			I2 = np.abs(lr.core.stft(y2, n_fft=self.frameSize, hop_length=self.hopSize))**2

			tau12ref = tdoas[0,0] - tdoas[0,1]

			for iSrc in range(0, nSrcs):

				tau12 = tdoas[iSrc,0] - tdoas[iSrc,1]

				dtau = np.abs(tau12 - tau12ref)

				gain = 1.0 - 1.0 / (1.0 + np.exp(-1.0 * self.alpha * (dtau - self.beta)))

				x1 = xs[iSrc,0,:]
				x2 = xs[iSrc,1,:]

				y1 += x1
				y2 += x2

				X1 = lr.core.stft(x1, n_fft=self.frameSize, hop_length=self.hopSize)
				X2 = lr.core.stft(x2, n_fft=self.frameSize, hop_length=self.hopSize)

				T1 += np.abs(gain * X1)**2
				T2 += np.abs(gain * X2)**2
				I1 += np.abs(X1)**2
				I2 += np.abs(X2)**2

			Y1 = lr.core.stft(y1, n_fft=self.frameSize, hop_length=self.hopSize)
			Y2 = lr.core.stft(y2, n_fft=self.frameSize, hop_length=self.hopSize)

			M1 = T1 / (I1 + self.epsilon)
			M2 = T2 / (I2 + self.epsilon)

			Y12 = Y1 * np.conj(Y2)

			k = np.expand_dims(np.arange(0, self.frameSize/2+1), axis=1)
			f = np.ones((1, Y12.shape[1]), dtype=np.float32)
			A = np.exp(-1j*2*np.pi*tau12ref*k*f/self.frameSize)

			X12 = np.transpose(A * Y12)
			M12 = np.transpose(M1 * M2)

			X = np.zeros((X12.shape[0],X12.shape[1],2), dtype=np.float32)
			X[:,:,0] = np.log(np.abs(X12)**2 + self.epsilon) - np.log(self.epsilon)
			X[:,:,1] = np.angle(X12)

			M = M12

			if file_scratch != "":

				np.savez(file_scratch, X=X, M=M)

		else:

			data = np.load(file_scratch)

			X = data['X']
			M = data['M']

		return X, M

