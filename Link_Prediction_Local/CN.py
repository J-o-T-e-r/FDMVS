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


def CN(Matrix):
    """

    :param Matrix: 邻接矩阵
    :return: 返回相似度矩阵
             对预测边按照相似度大小进行排序
    """
    StartTime = time.perf_counter()
    # 广义 jaccard 系数 两矩阵的点乘
    # 第一个矩阵中与该元素行号相同的元素与第二个矩阵与该元素列号相同的元素，两两相乘后再求和 表示A和B对应位都是1的属性的数量的矩阵
    Matrix_similarity = np.dot(Matrix, Matrix)

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
    fp1 = open('../Json/CN_similar.json', 'w+')
    fp1.write(doc)
    fp1.close()

    EndTime = time.perf_counter()
    print(f"Common Neighbours SimilarityTime: {EndTime - StartTime} s")
    return Matrix_similarity


