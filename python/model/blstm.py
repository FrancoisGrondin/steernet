import torch
import torch.nn as nn
import torch.nn.functional as F
import json

class Blstm(nn.Module):

	def __init__(self, file_json):

		super(Blstm, self).__init__()

		with open(file_json, 'r') as f:
			params = json.load(f)

		self.frame_size = params['frame_size']
		self.hidden_size = 128

		self.bn = nn.BatchNorm2d(num_features=2)

		self.lstm = nn.LSTM(input_size=int(self.frame_size/2+1)*2, 
							hidden_size=self.hidden_size, 
							num_layers=2,
							dropout=0.2,
							batch_first=True,
							bidirectional=True)

		self.fc = nn.Conv2d(in_channels=self.hidden_size*2,
							out_channels=int(self.frame_size/2+1),
							kernel_size=1)

	def forward(self, x):

		# Permute: N x T x F x 2 > N x 2 x T x F
		x = x.permute(0,3,1,2)

		# Batch norm: N x 2M x T x F > N x 2M x T x F
		x = self.bn(x)

		# Permute: N x 2M x T x F > N x T x F x 2M
		x = x.permute(0,2,3,1)

		# View: N x T x F x 2M > N x T x 2FM
		x = torch.reshape(x, (x.shape[0], x.shape[1], x.shape[2]*x.shape[3]))

		# LSTM: N x T x 2FM > N x T x 2H
		x, _ = self.lstm(x)

		# Permute: N x T x 2H > N x 2H x T
		x = x.permute(0,2,1)

		# Unsqueeze: N x 2H x T > N x 2H x T x 1
		x = torch.unsqueeze(x, 3)

		# FC: N x 2H x T x 1 > N x F x T x 1
		x = self.fc(x)

		# Permute: N x F x T x 1 > N x 1 x T x F
		x = x.permute(0,3,2,1)

		# Squeeze: N x 1 x T x F > N x T x F
		x = torch.squeeze(x, dim=1)

		# Set between 0 and 1
		x = torch.sigmoid(x)

		return x