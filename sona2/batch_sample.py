from sample import downsampleWav,downsampleWav1
import scipy.io.wavfile as wf
# import librosa
import  os


def resample(inpath,outrate,outpath):
    outrate = int(outrate)
    file = inpath.split('/')[-1]
    if inpath.endswith('.wav'):
        try:
            sample,sig = wf.read(inpath)
            manner = len(sig.shape)
            if manner == 1:
               downsampleWav1(inpath, outpath+'/sample_'+file, inrate=int(sample), outrate=outrate)
               return 'true'
            elif manner == 2:
               downsampleWav(inpath, outpath+'/sample_'+file, inrate=int(sample), outrate=outrate)
               return 'true'
        except:
            return 'error'
def resample2(inpath,outrate,outpath):
       wav_list = sorted([i for i in os.listdir(inpath) if i.endswith('.wav')])
       for i in wav_list:
           print(inpath+'/'+i)
           try:
               sample,sig = wf.read(inpath+'/'+i)
           except:
               return 'waverror'
           manner = len(sig.shape)
           if manner == 1:
               downsampleWav1(inpath+'/'+i,outpath+'/'+i,inrate=int(sample),outrate=int(outrate))

           elif manner == 2:
               downsampleWav(inpath+'/'+i,outpath+'/'+i,inrate=int(sample),outrate=int(outrate))

           else:
               return 'patherror'
       return 'true'
# for clean_file in clean_list:
#     file_path =  clean_path+clean_file
#     out_path = 'clean_train_wav/'+clean_file
#     downsampleWav(file_path,out_path,inrate=600, outrate=16000)
#
# for noise_file in noise_list:
#     file_path = noise_path+noise_file
#     out_path = 'noise_train_wav/'+noise_file
#     downsampleWav1(file_path,out_path,inrate=44100,outrate=16000)



