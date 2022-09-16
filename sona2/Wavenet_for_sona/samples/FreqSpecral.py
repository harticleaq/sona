from analysisdata import DataAnalysis

import matplotlib.pyplot as plt

clean_path = './samples_10/res60_noise6_clean.wav'
noisy_path = './samples_10/res60_noise6_noisy_5dB.wav'
denoise_path = './samples_10/res60_noise6_denoised_11dB.wav'

data_clean = DataAnalysis(clean_path)
data_noisy = DataAnalysis(noisy_path)
data_denoise = DataAnalysis(denoise_path)

length = len(data_noisy.sigs)

plt.subplot(221)
plt.title('clean')
plt.plot(data_clean.times[:length],data_clean.sigs[:length])

plt.subplot(222)
plt.title('noisy')
plt.plot(data_noisy.times[:length],data_noisy.sigs[:length])



plt.subplot(223)
plt.title('denoise')
plt.plot(data_denoise.times[:length],data_denoise.sigs[:length])

plt.tight_layout()
plt.show()
