import librosa
import numpy as np
import matplotlib.pyplot as plt

# Load audio file
y, sr = librosa.load('Saxophone.wav', sr=22050, duration=21)

# Calculate STFT
stft = librosa.stft(y, hop_length=512)
freqs = librosa.fft_frequencies(sr=sr, n_fft=stft.shape[1])

# Estimate fundamental frequency using YIN
f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=80, fmax=800, hop_length=512)

# Number of harmonics to analyze
n_harmonics = 10

# Initialize lists to store harmonic frequencies and standard deviations
harmonic_freqs = np.zeros((n_harmonics, len(f0)))
harmonic_stds = np.zeros(len(f0))

# Iterate through time frames
for i, f in enumerate(f0):
    if voiced_flag[i]:
        # Calculate expected harmonic frequencies
        harmonics = f * np.arange(1, n_harmonics + 1)

        # Find closest frequency bins in STFT
        harmonic_bins = np.argmin(np.abs(freqs[:, None] - harmonics), axis=0)

        # Extract harmonic frequencies from STFT
        harmonic_freqs[:, i] = freqs[harmonic_bins]

        # Extract harmonic amplitudes
        harmonic_amps = np.abs(stft[harmonic_bins, i])

        # Calculate standard deviation for each harmonic
        harmonic_stds[i] = np.average(np.std(harmonic_freqs, axis=1), weights=harmonic_amps)

# Plot spectrogram and weighted average standard deviation
plt.figure(figsize=(12, 8))

# Plot spectrogram
plt.subplot(2, 1, 1)
librosa.display.specshow(librosa.amplitude_to_db(np.abs(stft), ref=np.max),
                         y_axis='log', x_axis='time', hop_length=512)
plt.colorbar(format='%+2.0f dB')
plt.title('Spectrogram')

# Plot weighted average standard deviation
plt.subplot(2, 1, 2)
plt.plot(librosa.frames_to_time(np.arange(len(harmonic_stds)), hop_length=512), harmonic_stds)
plt.xlabel('Time (s)')
plt.ylabel('Weighted Average Standard Deviation')
plt.title('Weighted Average Standard Deviation of Harmonics')

plt.tight_layout()
plt.show()
