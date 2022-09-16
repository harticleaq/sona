import numpy as np
import numpy.fft as nf
import matplotlib.pyplot as plt
import scipy.io.wavfile as wf
# import displaywave
# from pylab import *
# mpl.rcParams['font.sans-serif'] = ['SimHei']
# mpl.rcParams['axes.unicode_minus'] = False

class FflNoise():
    def __init__(self,url):
        self.url = url
        self.sameple_rate,self.sigs = wf.read(self.url)

        self.N = len(self.sigs)
        self.asile = len(self.sigs.shape)
        if len(self.sigs.shape) >1:
            self.sigs = self.sigs.reshape(-1)
        self.sigs = (self.sigs)/(2**15)



        self.times = np.arange(len(self.sigs))/self.sameple_rate

        self.freqs = nf.fftfreq(self.sigs.size, 1/self.sameple_rate)
        self.complex_arry = nf.fft(self.sigs)

        self.pows = np.abs(self.complex_arry)
        self.mean = np.mean(self.pows)
        self.median = np.median(self.pows)

    def ffl_save(self,data,path):
        if self.asile >1:
            data = data.reshape(-1,2)
        data = data*(2**15)
        data = data.astype('i2')#格式转换
        wf.write(path,self.sameple_rate,data)


    def get_freq(self,freq_num):
        N = int(self.N*int(freq_num)/100)
        freqs_idx = self.pows.argsort()[-N:]
        freq = self.freqs[freqs_idx]
        return freq
    def get_sigs(self):
        return [self.times,self.sigs]
    def meanffl(self,scale):
        scale = int(scale*self.N/100)
        noised_idx = np.where( self.pows <self.mean)[0] #获取所有噪声的下标
        ca = self.complex_arry[:]
        ca[noised_idx] = 0+0j #高通滤波
        filter_sigs = nf.ifft(ca)
        return [self.times[:scale],self.sigs[:scale],filter_sigs[:scale]]

    def medianffl(self,scale):
        scale = int(scale*self.N/100)
        noised_idx = np.where( self.pows <self.median)[0] #获取所有噪声的下标
        ca = self.complex_arry[:]
        ca[noised_idx] = 0+0j #高通滤波
        filter_sigs = nf.ifft(ca)
        return [self.times[:scale],self.sigs[:scale],filter_sigs[:scale]]

    def ffl(self,scale,freq_num):
        lenth = int(self.N*scale/100)
        N = int(self.N*int(freq_num)/100)
        ca = self.complex_arry[:]
        noise_idx = self.pows.argsort()[:-N]

        ca[noise_idx] = 0+0j

        filter_sigs = nf.ifft(ca)
        return [self.times[:lenth],self.sigs[:lenth],filter_sigs[:lenth]]

        # fun_freq = freqs[pows.argsort()[-freq_num:]] #获取频率域中能量最高的
        # print(fun_freq)
        # noised_idx = np.where( pows <energy_value)[0] #获取所有噪声的下标
        #
        # ca[noised_idx] = 0+0j #高通滤波


        # filter_pows = np.abs(complex_arry)

        # plt.subplot(224)
        # plt.ylabel('power',fontsize=12)
        # plt.grid(linestyle=':')
        # plt.plot(freqs[freqs>0],filter_pows[freqs>0],color='dodgerblue',label='Filter Freq')
        # plt.legend()
        # #================第4步==============================================



        # plt.subplot(211)
        # plt.title('Time Domain',fontsize=16)
        # plt.ylabel('Signal',fontsize=12)
        #
        # plt.plot(times[:scale],sigs[:scale],label='Filter Signal')
        # plt.legend()
        # plt.subplot(212)
        # plt.title('Time Domain',fontsize=16)
        # plt.ylabel('Signal',fontsize=12)
        #
        # plt.plot(times[:scale],filter_sigs[:scale],color='dodgerblue',label='Filter Signal')
        # plt.legend()
        # plt.tight_layout()
        #
        # plt.show()

        # sameple_rate,sigs = wf.read(url)
        #
        # times = np.arange(len(sigs))/sameple_rate#时间=信号点数量/采样频率
        #
        # ft_y=np.fft.fft(sigs)
        #
        # n = len(sigs)
        #
        # #取得最大的振幅的二分之一
        # avg=np.max(abs(ft_y[1:]))/4
        #
        # ft_y[np.where(abs(ft_y)<=avg)]=0+0j
        #
        # data=np.fft.ifft(ft_y)

    # ffl('./20200112112429   3   6-0.0.wav',200,10,20)
