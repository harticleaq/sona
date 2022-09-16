import scipy.io.wavfile as wf
import matplotlib.pyplot as plt
import numpy as np

def karmanfilter(url,value,scale):
    sameple_rate,sigs = wf.read(url)
    sigs = sigs/(2**15)
    sigs = sigs.reshape(-1)
    times = np.arange(len(sigs))/sameple_rate
    length = int(len(times)*scale/100)
    Z = np.mat(sigs)


    '''
    定义状态向量X的初始状态
    X中包含两个状态变量：p和v，二者都被初始化为0，且二者都用标量表示
    '''
    X = np.mat([0])


    '''
    定义初始状态协方差矩阵P
    '''
    P = np.mat([1])

    '''
    定义状态转移矩阵F，假设每秒钟采一次样，所以delta_t = 1
    '''
    F = np.mat([1])

    '''
    定义状态转移协方差矩阵Q
    这里把协方差设置的很小，觉得状态转移矩阵准确度高
    '''
    Q = np.mat([value])

    '''
    定义观测矩阵H
    '''
    # H = np.mat([1, 0])

    '''
    定义观测噪声协方差R
    '''
    R = np.mat([0.01])

    '''
    卡尔曼滤波算法的预测和更新过程
    '''
    T = []
    for i in range(length):
        x_predict = F * X#demo中没有引入控制矩阵B
        p_predict = F * P * F.T +Q
        K = p_predict  / ( p_predict  + R)
        X = x_predict + K *(Z[0, i] -  x_predict)
        P = (np.eye(1) - K ) * p_predict
        T.append(X.item())
    return [times[:length],sigs[:length],T[:length]]
