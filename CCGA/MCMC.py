# -*- coding: utf-8 -*- 
# Time : 2021/7/30 11:20 
# Author : Kristina 
# File : MCMC.py
# contact: kristinaNFQ@163.com
# MyBlog: kristina100.github.io
# -*- coding:UTF-8 -*-

from collections import Counter
import numpy as np
import pandas as pd
import networkx as nx
from node2vec import Node2Vec
import operator

# from sklean.metrics import roc_auc_score

_data = pd.read_csv('../data/train.csv')
_v_1 = []
_v_2 = []
for i in range(1, _data.shape[0]):
    _v_1.append(_data['7718'][i])
    _v_2.append(_data['5688'][i])
MaxNodeNum = 10755
"""
    基于node2vec的随机游走模型
    得到了以每个节点开始的随机游走
    得到的社区
"""


def _node2vec(data, v_1, v_2):
    edges = []
    for i in range(data.shape[0]):
        link = (str(v_1[i]), str(v_2[i]))
        edges.append(link)

    # 制作无向图
    G = nx.Graph()
    for edge in edges:
        G.add_edge(edge[0], edge[1])
    G.to_undirected()
    node2vec = Node2Vec(G, emb_size=128, p=4, q=1, length_walk=50, num_walks=10, window_size=10, num_iters=2)
    walks = node2vec.random_walk()

    # 社区标记
    c_walk = {}
    i = 0
    for walk in walks:
        c_walk[i] = walk
        i += 1

    return c_walk


""" 返回结点的函数 """


def K(newZ, i):
    for item in newZ:
        if i == newZ[0]:
            return item[1]


def returnTuple(data, v_1, v_2):
    Sort1 = data[v_1].value_counts()
    Sort2 = data[v_2].value_counts()
    classCount1 = Sort1.to_dict()
    classCount2 = Sort2.to_dict()
    X, Y = Counter(classCount1), Counter(classCount2)
    z = dict(X + Y)

    # 按照id进行排序
    newZ = sorted(z.items(), key=lambda d: d[1], reverse=True)
    return newZ


""" 
    Agent 函数 
    论文思想--基于马尔科夫的随机游走的初始个体生成算法
    但是没有使用
    我使用的是node2vec
"""


def Agent(data, v_1, v_2):
    Sort1 = data[v_1].value_counts()
    Sort2 = data[v_2].value_counts()
    classCount1 = Sort1.to_dict()
    classCount2 = Sort2.to_dict()
    X, Y = Counter(classCount1), Counter(classCount2)
    z = dict(X + Y)

    # 按照id进行排序
    newZ = sorted(z.items(), key=lambda d: d[1], reverse=True)

    # 步骤一 在网络中随机选择目的节点，并计算P = {p1,p2,p3,...,pn}
    Dict = {}
    for key, value in z.items():
        Dict[key] = value / 10755
    New_tuple = sorted(Dict.items(), key=lambda d: d[0], reverse=False)
    List = []
    for item in range(len(New_tuple)):
        List.append(New_tuple[item][1])
    List = np.array(List)
    List.shape = (List.shape[0], 1)
    List_T = List.T
    temp = List + List_T

    """计算Q函数"""
    # m 指节点个数
    MaxNodeNum = 10756

    # 邻接矩阵
    MatrixNear = np.zeros([MaxNodeNum, MaxNodeNum])
    for col in range(1, data.shape[0]):
        i = int(data['7718'][col])
        j = int(data['5688'][col])
        MatrixNear[i, j] = 1
        MatrixNear[j, i] = 1
    # 社区
    C = _node2vec(data, v_1, v_2)

    Dict_Q = {}
    # 设置分裂点
    for i in range(1, data.shape[0]):
        sum = 0
        Q_0 = 0
        for j in range(1, data.shape[0]):
            if C[i] == C[j]:
                sum = sum
            else:
                sum += int(MatrixNear[i, j]) - K(newZ, i) * K(newZ, j) / (2 * MaxNodeNum)
                Q = 1 / (2 * MaxNodeNum) * sum
                if Q_0 < Q:
                    Q_0 = Q
                else:
                    break


"""
    交叉算子
"""


# 计算边结合度
def rangeNum(newZ):
    Cvw_Num = {}
    for v in range(1, 10755):
        num = 0
        for w in range(1, 10755):
            if (v, w) in newZ:
                num += 1
        Cvw = num / MaxNodeNum
        Cvw_Num[v] = Cvw
    return Cvw_Num


# 按照边结合度降序排序
def sortCvmNum(Cvm_num):
    # 使用operator的itemgetter进行排序
    Cvm = sorted(Cvm_num.items(), key=operator.itemgetter(1))
    return Cvm


"""
遗传和变异算子
"""

""" CCGA 算法"""
