

import librosa
import soundfile as sf

import matplotlib.pyplot as plt
import numpy as np
import math

file_path = '2.mp3'
#
#
signal, sr = librosa.load(file_path, sr = 16000)

RMS=math.sqrt(np.mean(signal**2))

STD_n= 0.101
noise=np.random.normal(0, STD_n, signal.shape[0])
#
# # X=np.fft.rfft(noise)
# # radius,angle=to_polar(X)
#
#print(signal)
#signal_noise = signal+noise

signal_noise = []
for v in signal:
	if v < 0:
		signal_noise.append(v + 0.8)
	else:
		signal_noise.append(v - 0.8)



# librosa.output.write_wav("8.wav", signal_noise, sr=16000, norm=False)
sf.write('3.wav', signal_noise, 16000)