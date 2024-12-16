import librosa
import matplotlib.pyplot
import matplotlib.pyplot as plt
import sklearn.decomposition
import numpy as np

# TODO: Find notes being played and then find overtone series. After that find the standard deviation
#  of each tone then average the standard deviation with the overtones weighted by decible level for tone

harmonicQuality = 32

y, sr = librosa.load("fantasia.wav", duration=20)
S = np.abs(librosa.stft(y))
times = librosa.times_like(S, sr=sr)

stft = librosa.stft(y, hop_length=512)

f0, voicing, voicing_probability = librosa.pyin(y=y, sr=sr, fmin=50, fmax=800)

harmonic_frequencies = np.zeros((harmonicQuality, len(f0)))
harmonic_standardDeviations = np.zeros(harmonicQuality)

for i, f in enumerate(f0):
    if voicing[i]:
        harmonics = f * np.arange(1, harmonicQuality + 1)
        freqs = librosa.fft_frequencies(sr=sr, n_fft=stft.shape[1])
        harmonic_bins = np.argmin(np.abs(freqs[:, None] - harmonics), axis=0)

        # Extract harmonic frequencies from STFT
        harmonic_frequencies[:, i] = freqs[harmonic_bins]

for g in range(harmonicQuality):
    harmonic_standardDeviations[g] = np.std(harmonics[g])

comps, acts = librosa.decompose.decompose(S, n_components=16, sort=True)
maxs = acts.max(axis=0)


T = sklearn.decomposition.MiniBatchDictionaryLearning(n_components=16)

scomps, sacts = librosa.decompose.decompose(S, transformer=T, sort=True)

layout = [list(".AAAA"), list("BCCCC"), list("DDDDD")]
fig, ax = plt.subplot_mosaic(layout, constrained_layout=True)
img = librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max),
                         y_axis='log', x_axis='time', ax=ax['A'])
ax['A'].set(title='Input spectrogram')
ax['A'].label_outer()
ax['A'].plot(times, f0, linewidth=2, color='white', label='f0')
librosa.display.specshow(librosa.amplitude_to_db(comps,
                                                 ref=np.max),
                         y_axis='log', ax=ax['B'])
ax['B'].set(title='Components')
ax['B'].label_outer()
ax['B'].sharey(ax['A'])
librosa.display.specshow(acts, x_axis='time', ax=ax['C'], cmap='gray_r')
ax['C'].set(ylabel='Components', title='Activations')
ax['C'].sharex(ax['A'])
ax['C'].label_outer()
ax['D'].plot(np.arange(harmonicQuality), harmonic_standardDeviations, color='red', label='Avg. Std. Dev.')
ax['D'].xlabel('Harmonic Number')
ax['D'].ylabel('Average Standard Deviation')
ax['D'].legend()

fig.colorbar(img, ax=list(ax.values()), format="%+2.f dB")  # Show the reference
matplotlib.pyplot.show()
