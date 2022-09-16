import wave
def pcmcope(pcm_path,waveaisle,sample,savepath):

    with open(pcm_path, 'rb') as pcmfile:
        pcmdata = pcmfile.read()

    a = pcm_path.split('/')[-1]
    a = a[:-4]
    a = savepath+'/'+a
    with wave.open(a + '.wav', 'wb') as wavfile:
        wavfile.setparams((waveaisle, 2, sample ,0, 'NONE', 'NONE')) #通道，量化位数，采样频率

        wavfile.writeframes(pcmdata)


