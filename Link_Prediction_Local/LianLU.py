# -*- coding: utf-8 -*- 
# Time : 2021/7/29 22:38
# Author : Kristina
# File : CN.py
# contact: kristinaNFQ@163.com
# MyBlog: kristina100.github.io
# -*- coding:UTF-8 -*-


import pandas as pd
import numpy as np
from Link_Prediction import AA, CN, cOS, HDI, HPI, Jaccard, LHN, PA, RA
from Indicators import auc_jaccard, Accuracy


_data = pd.read_csv('../data/train.csv')
data_test = pd.read_csv('../data/test.csv')


def Data_Shape(_data):
    """

    :param _data:
    :return:
    """
    MaxNodeNum = 10756
    return MaxNodeNum


def MatrixAdjacency0(MaxNodeNum, Data):
    """

    :param MaxNodeNum: 节点数总和
    :param Data: 训练集（测试集）
    :return: 返回邻接矩阵
    """
    MatrixAdjacency = np.zeros([MaxNodeNum, MaxNodeNum])
    for col in range(1, Data.shape[0]):
        i = int(Data['7718'][col])
        j = int(Data['5688'][col])
        MatrixAdjacency[i, j] = 1
        MatrixAdjacency[j, i] = 1
    return MatrixAdjacency


def MatrixAdjacency1(MaxNodeNum, Data):
    """

    :param MaxNodeNum: 节点总数
    :param Data: 训练集（测试集）
    :return: 返回邻接矩阵
    """
    MatrixAdjacency = np.zeros([MaxNodeNum, MaxNodeNum])
    for col in range(1, Data.shape[0]):
        i = int(Data['7043'][col])
        j = int(Data['7048'][col])
        MatrixAdjacency[i, j] = 1
        MatrixAdjacency[j, i] = 1

    return MatrixAdjacency


if __name__ == '__main__':
    MaxNodeNum = Data_Shape(_data)
    # 训练集的邻接矩阵
    MatrixNear_train = MatrixAdjacency0(MaxNodeNum, _data)
    # 测试集的邻接矩阵
    MatrixNear_test = MatrixAdjacency1(MaxNodeNum, data_test)
    # Adamic–Adar Index
    similar_AA = AA.AA(MatrixNear_train)
    auc_jaccard.AUC(MatrixNear_train, MatrixNear_test, similar_AA)
    Accuracy.prescision(MatrixNear_train, MatrixNear_test, similar_AA)
    # Preferential Attachment
    similar_PA = PA.PA(MatrixNear_train)
    auc_jaccard.AUC(MatrixNear_train, MatrixNear_test, similar_PA)
    Accuracy.prescision(MatrixNear_train, MatrixNear_test, similar_PA)
    # Resource Allocation Index
    similar_RA = RA.RA(MatrixNear_train)
    auc_jaccard.AUC(MatrixNear_train, MatrixNear_test, similar_RA)
    Accuracy.prescision(MatrixNear_train, MatrixNear_test, similar_RA)
    # Leicht-Holme-Newman Index
    similar_LHN = LHN.LHN(MatrixNear_train)
    auc_jaccard.AUC(MatrixNear_train, MatrixNear_test, similar_LHN)
    Accuracy.prescision(MatrixNear_train, MatrixNear_test, similar_LHN)
    # Hub Depressed Index
    similar_HDI = HDI.HDI(MatrixNear_train)
    auc_jaccard.AUC(MatrixNear_train, MatrixNear_test, similar_HDI)
    Accuracy.prescision(MatrixNear_train, MatrixNear_test, similar_HDI)
    # Hub Promoted Index
    similar_HPI = HPI.HPI(MatrixNear_train)
    auc_jaccard.AUC(MatrixNear_train, MatrixNear_test, similar_HPI)
    Accuracy.prescision(MatrixNear_train, MatrixNear_test, similar_HPI)
    # Jaccard Index
    similar_Jaccard = Jaccard.Jaccard(MatrixNear_train)
    auc_jaccard.AUC(MatrixNear_train, MatrixNear_test, similar_Jaccard)
    Accuracy.prescision(MatrixNear_train, MatrixNear_test, similar_Jaccard)
    # Common neighbours
    similar_CN = CN.CN(MatrixNear_train)
    auc_jaccard.AUC(MatrixNear_train, MatrixNear_test, similar_CN)
    Accuracy.prescision(MatrixNear_train, MatrixNear_test, similar_CN)
    # cosine
    similar_Cos = cOS.Cos(MatrixNear_train)
    auc_jaccard.AUC(MatrixNear_train, MatrixNear_test, similar_Cos)
    Accuracy.prescision(MatrixNear_train, MatrixNear_test, similar_Cos)
