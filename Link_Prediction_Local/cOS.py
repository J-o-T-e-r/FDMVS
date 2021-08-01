# -*- coding: utf-8 -*- 
# Time : 2021/7/29 22:38
# Author : Kristina
# File : CN.py
# contact: kristinaNFQ@163.com
# MyBlog: kristina100.github.io
# -*- coding:UTF-8 -*-


import numpy as np
import time
import json
import warnings
warnings.filterwarnings("ignore")


def Cos(Matrix):
    """

    :param Matrix: 邻接矩阵
    :return: 返回相似度矩阵
             对预测边按照相似度大小进行排序
    """
    StartTime = time.perf_counter()

    Matrix_D = np.diag(sum(Matrix))
    Matrix_Laplacian = Matrix_D - Matrix
    INV_Matrix_Laplacian = np.linalg.pinv(Matrix_Laplacian)

    Array_Diag = np.diag(INV_Matrix_Laplacian)
    Matrix_ONE = np.ones([Matrix.shape[0], Matrix.shape[0]])
    Matrix_Diag = Array_Diag * Matrix_ONE

    Matrix_similarity = INV_Matrix_Laplacian / ((Matrix_Diag * Matrix_Diag.T) ** 0.5)
    Matrix_similarity = np.nan_to_num(Matrix_similarity)

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
        List = sorted(List.items(), key=lambda item:item[1])
        All_dict[i] = List
    doc = json.dumps(All_dict)
    fp1 = open('../Json/Cos_similar.json', 'w+')
    fp1.write(doc)
    fp1.close()

    EndTime = time.perf_counter()
    print(f"Cosine SimilarityTime: {EndTime - StartTime}")
    return Matrix_similarity

