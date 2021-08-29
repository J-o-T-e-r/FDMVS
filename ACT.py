#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    ：ACT.py
@Author  ：wkml4996
@Date    ：2021/7/29 16:01 
"""
import json
import numpy as np
import pandas as pd
import math

data = pd.read_csv('train.csv', names=['V1', 'V2'])
test = pd.read_csv('test.csv', names=['V1', 'V2'])

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
for v1 in range(L_mat_.shape[0]):
    for v2 in range(L_mat_.shape[0]):
        sim_ACT[v1][v2] = 1 / (L_mat_[v1][v1] + L_mat_[v2][v2] - L_mat_[v1][v2])

# 转换为字典
All_dict = {}
for i in range(1, sim_ACT.shape[0]):
    similarList = list(sim_ACT[i])
    List = {}
    for j in range(len(similarList)):
        if similarList[j] > 0:
            if i == j:
                continue
            else:
                List[j] = similarList[j]
        else:
            continue
    # 用字典进行排序
    # 先转换为可迭代对象，也就是转化为元组，然后确定，元组的第几个元素进行比较
    List = sorted(List.items(), key=lambda item: (item[1], item[0]), reverse=True)
    All_dict[i] = List
doc = json.dumps(All_dict)
fp1 = open('sim_ACT.json', 'w+')
fp1.write(doc)
fp1.close()
