# import argparse, os, logging, random, time
# import numpy as np
# import math
# import time
# import scipy.sparse
# import lightgbm as lgb
# import torch
# import torch.nn as nn
# # import torchvision
# from torch.autograd import Variable

from train_models import *


    
def train_class(pre_data):
    parser = argparse.ArgumentParser(description='DeepGBM Models')
    parser.add_argument('-data', type=str, default='nipsA_offline')
    parser.add_argument('-model', type=str, default='gbdt2nn')

    parser.add_argument('-batch_size', type=int, default=128)
    parser.add_argument('-test_batch_size', type=int, default=50000)

    parser.add_argument('-seed', type=str, default='1,2,3,4,5')  # '1,2,3,4,5'
    parser.add_argument('-log_freq', type=int, default=100)
    parser.add_argument('-test_freq', type=int, default=3000)

    parser.add_argument('-l2_reg', type=float, default=1e-6)
    parser.add_argument('-l2_reg_opt', type=float, default=5e-4)
    parser.add_argument('-plot_title', type=str, default='paper_0127')

    """ python trainclass.py -data nipsA_offline -batch_size 4096 -plot_title 'paper_0127' -max_epoch 30 -nslices 20 -ntrees 200 
    -tree_layers 100,100,100,50 -emb_epoch 2 -maxleaf 128 -embsize 20 -emb_lr 1e-3 -lr 1e-3 -opt Adam -loss_de 3 -loss_dr 0.9 
    -loss_init 0.9 -test_batch_size 50000 -group_method Random -model d1 -feat_per_group 128  -tree_lr 0.15 -l2_reg 1e-6 -test_freq 3000 
    -cate_layers 32,32 -seed 1,2,3,4,5"""

    parser.add_argument('-emb_epoch', type=int, default=2)
    parser.add_argument('-emb_lr', type=float, default=1e-3)
    parser.add_argument('-emb_opt', type=str, default="Adam")

    parser.add_argument('-nslices', type=int, default=20)
    parser.add_argument('-ntrees', type=int, default=100)

    parser.add_argument('-tree_layers', type=str, default="100,100,100,50")
    parser.add_argument('-cate_layers', type=str, default="32,32")

    parser.add_argument('-maxleaf', type=int, default=128)
    parser.add_argument('-mindata', type=int, default=40)
    parser.add_argument('-tree_lr', type=float, default=0.15)
    parser.add_argument('-embsize', type=int, default=20)
    parser.add_argument('-cate_embsize', type=int, default=4)

    parser.add_argument('-lr', type=float, default=1e-3)
    parser.add_argument('-opt', type=str, default='AdamW')

    parser.add_argument('-max_epoch', type=int, default=30)
    parser.add_argument('-loss_init', type=float, default=0.9)
    parser.add_argument('-loss_dr', type=float, default=0.9)

    parser.add_argument('-group_method', type=str, default='Random')
    parser.add_argument('-feature_emb_size', type=int, default=50)

    parser.add_argument('-feat_per_group', type=int, default=128)
    parser.add_argument('-loss_de', type=int, default=3)
    parser.add_argument('-task', type=str, default='regression')
    parser.add_argument('-kd_type', type=str, default='emb')

    args = parser.parse_args()
    assert (args.nslices <= args.ntrees)

    plot_title = args.data + "_" + args.opt + "_s" + str(args.seed) + "_ns" + str(args.nslices) + "_nt" + str(
        args.ntrees)
    plot_title += "_lf" + str(args.maxleaf)
    plot_title += "_lr" + str(args.lr) + "_lde" + str(args.loss_de) + "_ldr" + str(args.loss_dr)
    plot_title += "_" + args.model
    plot_title += "_emb" + str(args.embsize) + '_fpg' + str(args.feat_per_group)
    plot_title += '_' + args.plot_title
    plot_title += '_' + args.group_method

    args.seeds = [int(x) for x in args.seed.split(',')]
    random.seed(args.seeds[0])
    np.random.seed(args.seeds[0])
    # torch.cuda.manual_seed_all(args.seeds[0])
    cate_model_list = ['deepfm', 'pnn', 'wideNdeep', 'lr', 'fm']
    if args.model in cate_model_list:
        cate_data = dh.load_data(args.data+'_cate')
        # designed for fast cateNN
        cate_data = dh.trans_cate_data(cate_data)
        train_cateModels(args, cate_data, plot_title, key="")
    if "gbdt2nn" in args.model:
        print('gbdt model...')
        real_data_index = [3,4,5,6,9,10,11,12,14,15,16,17,18,19,20,21,23,24]
        num = dh.load_data(args.data+'_num')
        su = num[0][:,real_data_index]
        num_data = (su,num[1],num[2][:,real_data_index],num[3])
        _,_,_,pre_y = train_GBDT2NN(args, num_data, plot_title,'', pre_data, kd_type=args.kd_type)
        return pre_y
    elif args.model == "deepgbm":
        num_data = dh.load_data(args.data+'_num')
        cate_data = dh.load_data(args.data+'_cate')
        # designed for fast cateNN
        cate_data = dh.trans_cate_data(cate_data)
        train_DEEPGBM(args, num_data, cate_data, plot_title, key="")
    elif args.model == 'd1':
        num_data = dh.load_data(args.data+'_num')
        cate_data = dh.load_data(args.data+'_cate')
        # designed for fast cateNN
        cate_data = dh.trans_cate_data(cate_data)
        train_D1(args, num_data, cate_data, plot_title, key="")

