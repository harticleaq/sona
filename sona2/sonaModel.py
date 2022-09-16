import sys
import logging
import json
import os

from Wavenet_for_sona import denoise
from Wavenet_for_sona import util,dataset
from PyQt5 import QtWidgets

import torch
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import torch.optim as optim
from Wavenet_for_sona.dataset import sonaDataset
from Wavenet_for_sona.models import Wavenet,TrainingConfig,PredictConfig
import sys
sys.setrecursionlimit(50000)

def training(config):
    model = Wavenet(config)
    print('model loading ......')
    datasets = sonaDataset(config,model).load_dataset()
    print('dataset building...')

    num_train_samples = config['training']['num_train_samples']
    num_test_samples = config['training']['num_test_samples']

    train_set_generator = datasets.get_random_batch_generator('train')
    test_set_generator = datasets.get_random_batch_generator('test')

    train_set_iterator = dataset.denoising_dataset(train_set_generator)
    test_set_iterator = dataset.denoising_dataset(test_set_generator)

    train_loader = DataLoader(train_set_iterator, batch_size=None)
    valid_loader = DataLoader(test_set_iterator, batch_size=None)

    dataloader = {'train_loader':train_loader, 'valid_loader':valid_loader}
    training_config = TrainingConfig(model, dataloader, config)
    training_config.setup_model()
    print('model setup done...')
    training_config.train(num_train_samples, num_test_samples)
    print('model training done...')

def load_args(clean_path,noisy_path):
    #装载初始参数
    config = './Wavenet_for_sona/paras/config.json'
    #模式
    mode = 'inference'
    #模型路径
    load_checkpoint = './Wavenet_for_sona/checkpoints/config1_epoch0135.pth'
    #音频路径
    clean_input_path = clean_path
    noisy_input_path =  noisy_path
    option = {'config':config,'mode':mode,'load_checkpoint':load_checkpoint,'clean_input_path':
              clean_input_path,'noisy_input_path':noisy_input_path}
    return option

def load_config(url):
    with open(url,'r') as f:
        config = json.load(f)
        return config

def get_valid_output_folder_path(outputs_folder_path):
    j = 1
    while True:
        output_folder_name = 'samples_%d' % j
        output_folder_path = os.path.join(outputs_folder_path, output_folder_name)
        if not os.path.isdir(output_folder_path):
            os.makedirs(output_folder_path)
            break
        j += 1
    return output_folder_path

def inference(config,args,bar,edit):
    batch_size  = config['training']['batch_size']
    model = Wavenet(config)
    samples_folder_path = os.path.join(config['training']['path'], 'samples')
    output_folder_path = get_valid_output_folder_path(samples_folder_path)

    filenames = [filename for filename in os.listdir(args['noisy_input_path']) if filename.endswith('.wav')]
    clean_input = None
    count = 0
    sum_count = len(filenames)
    for filename in filenames:
        count+=1
        edit.append(f'正在处理文件：{filename}。-------第{count}/{sum_count}个。')
        QtWidgets.qApp.processEvents()
        noisy_input = util.load_wav(args['noisy_input_path'] + filename, config['dataset']['sample_rate'])
        if args['clean_input_path'] is not '':
            clean_input = util.load_wav(args['clean_input_path'] + filename[:5]+'.wav', config['dataset']['sample_rate'])

        inputs = {'noisy': noisy_input, 'clean': clean_input}
        print(len(noisy_input))
        output_filename_prefix = filename[0:-4] + '_'
        print("Denoising: " + filename)

        predict_config = PredictConfig(model, args['load_checkpoint'])
        denoise.denoise_sample(predict_config, inputs, batch_size, output_filename_prefix,
                                                config['dataset']['sample_rate'], output_folder_path,bar)

def main(clean_path,noisy_path, bar,edit):
    args = load_args(clean_path,noisy_path)
    config = load_config(args['config'])
    if args['mode']=='training':
        training(config)
    if args['mode']=='inference':
        inference(config,args,bar,edit)
#
# def showBar(w,bar,j):
#
#     b = QProgressBar(w)
#     for i in range(j):
#         b.setValue(i)
#         b.update()

