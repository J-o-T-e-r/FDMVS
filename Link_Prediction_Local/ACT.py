# -*- coding: utf-8 -*- 
# Time : 2021/7/29 22:37 
# Author : Kristina 
# File : ACT.py
# contact: kristinaNFQ@163.com
# MyBlog: kristina100.github.io
# -*- coding:UTF-8 -*-


import numpy as np
import pandas as pd
import json
import logging

FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
logging.basicConfig(filename='my.log', level=logging.DEBUG, format=FORMAT)
d = {'clientip': '192.168.0.1', 'user': 'fbloggs'}
logger = logging.getLogger('tcpserver')
logger.warning('Protocol problem: %s', 'connection reset', extra=d)

data = pd.read_csv('../data/train.csv', names=['V1', 'V2'])
test = pd.read_csv('../data/test.csv', names=['V1', 'V2'])

# 邻接矩阵
mat = np.zeros((10755, 10755))
for i in range(data.shape[0]):
    mat[data.iloc[i, 0] - 1, data.iloc[i, 1] - 1] += 1
    mat[data.iloc[i, 1] - 1, data.iloc[i, 0] - 1] += 1

# 权重矩阵
w_mat = np.zeros((10755, 10755))
for i in range(mat.shape[0]):
    w_mat[i][i] = np.sum(mat[i])

# 拉普拉斯矩阵
L_mat = w_mat - mat

L_mat_ = np.linalg.pinv(L_mat)

sim_ACT = np.zeros((10755, 10755))
Dict = {}
for v1 in range(L_mat_.shape[0]):
    List = []
    for v2 in range(L_mat_.shape[0]):
        sim_ACT[v1][v2] = 1 / (L_mat_[v1][v1] + L_mat_[v2][v2] - L_mat_[v1][v2])
        List.append(sim_ACT[v1][v2])
    Dict[v1] = List
doc = json.dumps(Dict)
fp1 = open('../Json/ACT.json', 'w+')
fp1.write(doc)
fp1.close()

