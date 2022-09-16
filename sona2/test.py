import numpy as np
import numpy.fft as nf
import matplotlib.pyplot as plt
import scipy.io.wavfile as wf

sameple_rate,sigs = wf.read('./20200112112429   3   6-0.0.wav')

len(sigs)
print('采样率:{}'.format(sameple_rate))
print('信号点数量:{}'.format(sigs.size))
sig_ = 10*np.log10(sigs)

sigs = sigs/(2**15)


times = np.arange(len(sigs))/sameple_rate

freqs = nf.fftfreq(sigs.size, 1/sameple_rate)
complex_arry = nf.fft(sigs)
pows = 10*np.log10(np.abs(complex_arry))






font={"family":"SimHei","style":"normal","weight":"normal","color":"green","size":16}
plt.rcParams["font.family"] = 'Arial Unicode MS'


figure = plt.figure(num="频谱图",figsize=(9,6))

ax = plt.subplot(2,2,1)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.xlabel('time(S)')
plt.ylabel('electric(V)')
plt.plot(times,sigs,label = 'elec')
plt.legend()
plt.title('Time')

ax = plt.subplot(2,2,2)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.xlabel('freq(Hz)')
plt.ylabel('energy(A)')
plt.plot(freqs,pows,label = 'amplitude',color = 'green')
plt.legend()
plt.title('你好')

ax = plt.subplot(2,2,3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.xlabel('time(S)')
plt.ylabel('electric(V)')
plt.plot(times,sig_,label = 'elec')
plt.legend()
plt.title('Time')
plt.tight_layout()

ax = plt.subplot(2,2,4)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.xlabel('time(S)')
plt.ylabel('electric(V)')
plt.plot(times,sigs,label = 'elec')
plt.legend()
plt.title('Time')
plt.show()
