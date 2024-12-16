import math

import numpy as np
import sounddevice as sd

fs = 44100  # Sample rate
duration = 3  # Duration in seconds
amountOfOvertones = 32
frequencies = [82.41 * i for i in range(1, amountOfOvertones)]
amplitudes = [math.log((amountOfOvertones-(i-1))/amountOfOvertones, math.e) for i in range(1, amountOfOvertones)]  # Amplitudes for each frequency
t = np.linspace(0, duration, int(fs * duration), False)

audio = np.zeros_like(t)
for i, freq in enumerate(frequencies):
    audio += amplitudes[i] * np.sin(2 * np.pi * freq * t)

audio /= np.max(np.abs(audio), axis=0)

if audio.ndim == 1:
    audio = audio.reshape(-1, 1)
sd.play(audio, samplerate=fs)
sd.wait()
