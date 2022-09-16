# import librosa
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wf
# mpl.rcParams['font.sans-serif'] = ['SimHei']
#
# mpl.rcParams['axes.unicode_minus'] = False
# from sona.fll2 import sameple_rate
import sonaui
def initUrl():
    pass

def plotPng():
    pass
def plotFreq():
    pass
def plotwave(url):
    u = url
    label = u.split('/')[-1][:-4]

    sameple_rate, sigs = wf.read(url)#audio 采样信号，freq采样率
    time = np.arange(len(sigs)) / sameple_rate
    plt.figure('Filter',facecolor='lightgray')
    plt.title('Time',fontsize=16)
    plt.ylabel('Signal',fontsize=12)

    plt.plot(time[:200],sigs[:200],color='dodgerblue',label='Noised Signal')
    plt.savefig('./'+label+".png")
    return

    # audio, freq = librosa.load(u)#audio 采样信号，freq采样率
    # time = np.arange(0, len(audio)) / freq
    # plt.figure('Filter',facecolor='lightgray')
    # plt.title('Filter',fontsize=16)
    # plt.xlabel('Time',fontsize=12)
    # plt.ylabel('Signal',fontsize =12)
    # plt.plot(time, audio,color='dodgerblue',label='Noised Signal')




