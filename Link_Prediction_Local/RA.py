# -*- coding: utf-8 -*- 
# @Time : 2021/7/28 14:23 
# @Author : kzl 
# @File : RA.py
# @contact: kristinaNFQ@gmail.com
import numpy as np
import pandas as pd
import time
import json
import LianLU
import warnings

warnings.filterwarnings("ignore")

_data = pd.read_csv('data/train.csv')

# 就是比aa少了个log
def RA(MatrixAdjacency_Train):
    similarity_StartTime = time.perf_counter()
    # (10756, )
    RA_Train = sum(MatrixAdjacency_Train)
    # (10756, 1)
    RA_Train.shape = (RA_Train.shape[0], 1)
    #  出现 nan 值
    MatrixAdjacency_Train = MatrixAdjacency_Train / RA_Train
    # 使用0代替数组x中的nan元素，使用有限的数字代替inf元素

    MatrixAdjacency_Train = np.nan_to_num(MatrixAdjacency_Train)
    # 求出了每个点在图中度数的导数的矩阵，然后再与原始数据相乘，得到id之间相乘后得到矩阵
    Matrix_similarity = np.dot(MatrixAdjacency_Train, MatrixAdjacency_Train)

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
    fp1 = open('Json/RA_similar.json', 'w+')
    fp1.write(doc)
    fp1.close()
    similarity_EndTime = time.perf_counter()
    print(f"SimilarityTime: {similarity_EndTime - similarity_StartTime} s")
    return Matrix_similarity


a = LianLU.Data_Shape(_data)
b = LianLU.MatrixAdjacency0(a, _data)
RA(b)