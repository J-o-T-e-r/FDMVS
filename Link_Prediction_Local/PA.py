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


def PA(Matrix):
    """

    :param Matrix: 邻接矩阵
    :return: 返回相似度矩阵
             对预测边按照相似度大小进行排序
    """
    StartTime = time.perf_counter()

    deg_row = sum(Matrix)
    deg_row.shape = (deg_row.shape[0], 1)
    deg_row_T = deg_row.T
    # k_x*k_y
    Matrix_similarity = np.dot(deg_row, deg_row_T)
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
    fp1 = open('Json/PA_similar.json', 'w+')
    fp1.write(doc)
    fp1.close()

    EndTime = time.perf_counter()

    print(f"Preferential Attachment SimilarityTime: {EndTime - StartTime} s")
    return Matrix_similarity

