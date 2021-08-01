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

# 就是比aa少了个log
def RA(Matrix):
    """

    :param Matrix: 邻接矩阵
    :return: 返回相似度矩阵
             对预测边按照相似度大小进行排序
    """
    similarity_StartTime = time.perf_counter()
    # (10756, )
    RA_Train = sum(Matrix)
    # (10756, 1)
    RA_Train.shape = (RA_Train.shape[0], 1)
    #  出现 nan 值
    MatrixAdjacency_Train = Matrix / RA_Train
    # 使用0代替数组x中的nan元素，使用有限的数字代替 inf 元素

    Matrix = np.nan_to_num(Matrix)
    # 求出了每个点在图中度数的导数的矩阵，然后再与原始数据相乘，得到id之间相乘后得到矩阵
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
    fp1 = open('../Json/RA_similar.json', 'w+')
    fp1.write(doc)
    fp1.close()
    similarity_EndTime = time.perf_counter()
    print(f" Resource Allocation Index SimilarityTime: {similarity_EndTime - similarity_StartTime} s")
    return Matrix_similarity

