import os

import numpy as np
import scipy.io.wavfile as wf
import numpy.fft as nf

class DataAnalysis():


    def __init__(self,url):
        self.sameple_rate,self.sigs_ = wf.read(url)
        self.name = url
        if len(self.sigs_.shape) == 1:
            self.aisle = 1
            self.sigs = self.sigs_
            self.calcuData(self.sigs)
        else:
            self.aisle = self.sigs_.shape[1]



    def calcuData(self,sigs):
        self.sigs = sigs
        self.num = self.sigs.size
        self.sigs =self.sigs/(2**15)
        self.times = np.arange(len(self.sigs))/self.sameple_rate
        self.freqs = nf.fftfreq(self.sigs.size, 1/self.sameple_rate)
        self.complex_arry = nf.fft(self.sigs)
        self.pows = np.abs(self.complex_arry)
            #时域参数
        N = len(self.sigs)
        self.TIME_MAX = np.max(self.sigs)
        self.TIME_MIN = np.min(self.sigs)
        self.TIME_MEDIAN = np.median(self.sigs)
        self.TIME_MEAN = np.mean(self.sigs)
        self.TIME_VAR = np.var(self.sigs)
        self.TIME_STD = np.std(self.sigs)
        self.TIME_PTP = np.ptp(self.sigs)
        self.TIME_RMS = np.sqrt(pow(self.TIME_MEAN,2) + pow(self.TIME_STD,2))

        temp1 = np.sum(pow(self.sigs-self.TIME_MEAN,3))
        temp2 = pow(np.sum(pow(self.sigs-self.TIME_MEAN,2))/(N-1),3/2)
        self.TIME_SKEW = temp1/((N)*temp2)

        temp1 = np.sum(pow(self.sigs-self.TIME_MEAN,4))
        temp2 = pow(np.sum(pow(self.sigs-self.TIME_MEAN,2))/N,2)
        self.TIME_KURT = temp1/((N)*temp2)-3

        self.TIME_KURT_FACTOR = self.TIME_MAX/self.TIME_RMS
        self.TIME_WAVE_FACTOR = self.TIME_RMS/self.TIME_MEAN,
        self.TIME_PULSE_FACTOR = self.TIME_MAX/abs(self.TIME_MEAN)
        self.TIME_MARGIN_FACTOR = self.TIME_MAX/pow(self.TIME_RMS,2)

        #频域参数
        self.FREQ_MAX = np.max(self.pows)
        self.FREQ_MIN = np.min(self.pows)
        self.FREQ_MEDIAN = np.median(self.pows)
        self.FREQ_MEAN = np.mean(self.pows)
        self.FREQ_VAR = np.var(self.pows)
        self.FREQ_STD = np.std(self.pows)
        self.FREQ_PTP = np.ptp(self.pows)

    def get_data(self):

        if self.aisle==1:

            self.spectrum = np.fft.fft(self.sigs)
            self.ceps = np.fft.ifft(np.log(np.abs(self.spectrum))).real
            return [self.sigs,self.times,self.freqs,self.pows,self.ceps]

        else:
            item = []
            sigs_0 = self.sigs_[:,0]

            self.calcuData(sigs_0)
            item.append(self.sigs)
            self.spectrum = np.fft.fft(self.sigs)
            self.ceps = np.fft.ifft(np.log(np.abs(self.spectrum))).real
            item.append(self.ceps)
            item.append(self.times)
            item.append(self.freqs)

            self.calcuData(self.sigs_[:,1])
            item.append(self.sigs)
            self.spectrum = np.fft.fft(self.sigs)
            self.ceps = np.fft.ifft(np.log(np.abs(self.spectrum))).real
            item.append(self.ceps)
            item.append(self.freqs)

            self.calcuData(self.sigs_.reshape(-1))
            item.append(self.freqs)
            item.append(self.pows)
            item.append(self.sigs)
            item.append(self.times)
            return item
    @staticmethod
    def getTimeLabel():
        time_label = ['文件名','时域/频域','量化位数','通道数','采样率','采样点总数','最大值','最小值','中心值','平均值','方差',
                           '标准差','峰差','均方根','偏度','峭度','峰度因子','波形因子','脉冲因子','裕度因子']
        return time_label
    def getAisle(self):
        return self.aisle

    def getTimes(self):
        if self.aisle == 1:
            item = [self.name,'时域','2',self.aisle,self.sameple_rate,self.num,self.TIME_MAX,self.TIME_MIN,self.TIME_MEDIAN,self.TIME_MEAN,self.TIME_VAR,self.TIME_STD,
                    self.TIME_PTP,self.TIME_RMS,self.TIME_SKEW,self.TIME_KURT,self.TIME_KURT_FACTOR,
                    self.TIME_WAVE_FACTOR[0],self.TIME_PULSE_FACTOR,self.TIME_MARGIN_FACTOR]
            return item
        else:
            sigs = self.sigs_[:,0]
            self.calcuData(sigs)
            item1 = [self.name,'左声道时域','2',self.aisle,self.sameple_rate,self.num,self.TIME_MAX,self.TIME_MIN,self.TIME_MEDIAN,self.TIME_MEAN,self.TIME_VAR,self.TIME_STD,
                    self.TIME_PTP,self.TIME_RMS,self.TIME_SKEW,self.TIME_KURT,self.TIME_KURT_FACTOR,
                    self.TIME_WAVE_FACTOR[0],self.TIME_PULSE_FACTOR,self.TIME_MARGIN_FACTOR]
            sigs = self.sigs_[:,1]
            self.calcuData(sigs)
            item2 = [self.name,'右声道时域','2',self.aisle,self.sameple_rate,self.num,self.TIME_MAX,self.TIME_MIN,self.TIME_MEDIAN,self.TIME_MEAN,self.TIME_VAR,self.TIME_STD,
                    self.TIME_PTP,self.TIME_RMS,self.TIME_SKEW,self.TIME_KURT,self.TIME_KURT_FACTOR,
                    self.TIME_WAVE_FACTOR[0],self.TIME_PULSE_FACTOR,self.TIME_MARGIN_FACTOR]

            items = [item1,item2]
            return items
    def getFreqs(self):
        if self.aisle == 1:
            item = [self.name,'频域','2',self.aisle,self.sameple_rate,self.num,self.FREQ_MAX,
                    self.FREQ_MIN,self.FREQ_MEDIAN,self.FREQ_MEAN,self.FREQ_VAR,
                    self.FREQ_STD,self.FREQ_PTP]
            return item
        else:
            sigs = self.sigs_[:,0]
            self.calcuData(sigs)
            item1 = [self.name,'左声道频域','2',self.aisle,self.sameple_rate,self.num,self.FREQ_MAX,
                    self.FREQ_MIN,self.FREQ_MEDIAN,self.FREQ_MEAN,self.FREQ_VAR,
                    self.FREQ_STD,self.FREQ_PTP]
            self.calcuData(sigs)
            item2 = [self.name,'左声道频域','2',self.aisle,self.sameple_rate,self.num,self.FREQ_MAX,
                    self.FREQ_MIN,self.FREQ_MEDIAN,self.FREQ_MEAN,self.FREQ_VAR,
                    self.FREQ_STD,self.FREQ_PTP]
            item = [item1,item2]
            return item

    #倒频谱


