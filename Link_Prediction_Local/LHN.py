# -*- coding: utf-8 -*- 
# @Time : 2021/7/28 15:16 
# @Author : kzl 
# @File : LHN.py
# @contact: kristinaNFQ@gmail.com

import numpy as np
import pandas as pd
import time
import json
import LianLU
import warnings
warnings.filterwarnings("ignore")

_data = pd.read_csv('data/train.csv')


def LHN(MatrixAdjacency_Train):
    similarity_StartTime = time.perf_counter()
    Matrix_similarity = np.dot(MatrixAdjacency_Train, MatrixAdjacency_Train)
    deg_row = sum(MatrixAdjacency_Train)
    deg_row.shape = (deg_row.shape[0], 1)
    deg_row_T = deg_row.T

    temp = np.dot(deg_row, deg_row_T)

    Matrix_similarity = Matrix_similarity / temp

    All_dict = {}
    for i in range(1, Matrix_similarity.shape[0]):
        similarList = list(Matrix_similarity[i])
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
    fp1 = open('Json/LHN_similar.json', 'w+')
    fp1.write(doc)
    fp1.close()

    similarity_EndTime = time.perf_counter()

    print(f"SimilarityTime: {similarity_EndTime - similarity_StartTime} s")
    return Matrix_similarity


a = LianLU.Data_Shape(_data)
b = LianLU.MatrixAdjacency0(a, _data)
LHN(b)