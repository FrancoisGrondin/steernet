from torch.utils.data import Dataset
import json
import librosa as lr
import numpy as np
import matplotlib.pyplot as plt

class Audio(Dataset):

	def __init__(self, file_meta):

		with open(file_meta) as f:
			self.elements = f.read().splitlines()

	def __len__(self):

		return len(self.elements)

	def __getitem__(self, idx):

		audio = json.loads(self.elements[idx])

		fs = 16000

		mics = audio['farfield']['mics']
		srcs = audio['farfield']['srcs']
		speed = audio['farfield']['speed']
		snrs = audio['farfield']['snr']
		gains = audio['farfield']['gain']
		volume = audio['farfield']['volume']
		path = audio['farfield']['path']
		noise = audio['farfield']['noise']

		hs, _ = lr.core.load(path=path, sr=16000, mono=False)

		nSrcs = len(srcs)
		nMics = len(mics)

		duration = audio['speech'][0]['duration']
		N = round(duration * fs)

		xs = np.zeros((nSrcs,nMics,N), dtype=np.float32)

		for iSrc in range(0, nSrcs):

			path = audio['speech'][iSrc]['path']
			offset = audio['speech'][iSrc]['offset']

			s, _ = lr.core.load(path=path, sr=fs, mono=True, offset=offset, duration=duration)

			snr = snrs[iSrc]

			for iMic in range(0, nMics):

				gain = gains[iMic]

				index = iSrc * nMics + iMic
				h = hs[index,:]

				x = np.convolve(h,s,mode='same')

				x /= np.sqrt(np.mean(x**2))
				x *= 10.0 ** (snr/20.0)
				x *= gain

				xs[iSrc,iMic,range(0,x.shape[0])] = x

		xs /= np.max(xs)
		xs *= volume

		ns = noise * np.random.randn(nMics,N)

		tdoas = np.zeros((nSrcs, nMics), dtype=np.float32)

		for iSrc in range(0, nSrcs):

			src = np.array(srcs[iSrc])
			src -= np.mean(np.array(mics), axis=0)
			src /= np.sqrt(np.sum(src**2))

			for iMic in range(0, nMics):

				mic = mics[iMic] - np.mean(np.array(mics), axis=0)
				tdoas[iSrc,iMic] = (fs/speed) * np.dot(mic, src)

		return xs, ns, tdoas