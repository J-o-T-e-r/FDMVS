# -*- coding: utf-8 -*- 
# @Time : 2021/7/27 8:35 
# @Author : kzl 
# @File : LianLU.py
# @contact: kristinaNFQ@gmail.com

"""

计算一对节点的分数,
该分数可看作为那些节点基于拓扑网络的“近似度”
两个节点越相近，它们之间存在联系的可能性就越大

Adamic Adar（AA 指标）
AA 指标也考虑了共同邻居的度信息，但除了共同邻居，
还根据共同邻居的节点的度给每个节点赋予一个权重，即度的对数分之一，
然后把每个节点的所有共同邻居的权重值相加，
其和作为该节点对的相似度值

节点的度指它的邻居数



Adamic Adar：计算共同邻居的度数的对数分之一，并求和。

优先连接算法：计算每个节点的度数的乘积。

资源分配算法：计算共同邻居的度数分之一，并求和。

共同社区算法：利用社区发现算法，检查两个节点是否处于同一个社区。


从网络中提取拓扑结构特征，运用机器学习方法进行链路预测，比较了几种机器学习算法的预测精度。
"""
from scipy import sparse
import pandas as pd
import numpy as np
import networkx as nx
oo = float('inf')

# 创建无向图
G = nx.Graph()
_data = pd.read_csv('data/train.csv')
data_test = pd.read_csv('data/test.csv')
_data.dropna(axis=0, how='any', inplace=True)
print(_data.shape[0])


def Data_Shape(_data):
    MaxNodeNum = 10756
    return MaxNodeNum


def MatrixAdjacency0(MaxNodeNum, Data):
    MatrixAdjacency = np.zeros([MaxNodeNum, MaxNodeNum])
    for col in range(1, Data.shape[0]):
        i = int(Data['7718'][col])
        j = int(Data['5688'][col])
        MatrixAdjacency[i, j] = 1
        MatrixAdjacency[j, i] = 1
    return MatrixAdjacency


def MatrixAdjacency1(MaxNodeNum, Data):
    MatrixAdjacency = np.zeros([MaxNodeNum, MaxNodeNum])
    for col in range(1, Data.shape[0]):
        i = int(Data['7043'][col])
        j = int(Data['7048'][col])
        MatrixAdjacency[i, j] = 1
        MatrixAdjacency[j, i] = 1

    return MatrixAdjacency

# MaxNodeNum = Data_Shape(data)
# # 训练集的邻接矩阵
# MatrixNear_train = MatrixAdjacency0(MaxNodeNum, data)
# # 测试集的邻接矩阵
# MatrixNear_test = MatrixAdjacency1(MaxNodeNum, data_test)
