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
import LianLU
import warnings

warnings.filterwarnings("ignore")


def Jaccard(Matrix):
    """

    :param Matrix: 邻接矩阵
    :return: 返回相似度矩阵
             对预测边按照相似度大小进行排序
    """
    StartTime = time.perf_counter()
    # 广义 jaccard 系数 两矩阵的点乘
    # 第一个矩阵中与该元素行号相同的元素与第二个矩阵与该元素列号相同的元素，两两相乘后再求和 表示A和B对应位都是1的属性的数量的矩阵
    Matrix_similarity = np.dot(Matrix, Matrix)
    # 原始数据的求和计算 构造了一个一维数组
    deg_row = sum(Matrix)
    # 新构造一个二维向量 （二维（10756，1））
    deg_row.shape = (deg_row.shape[0], 1)
    # 转置 便于计算（1，10756）
    deg_row_T = deg_row.T
    # 得到一个新的矩阵
    tempdeg = deg_row + deg_row_T
    # 得到的新矩阵减去相似矩阵  得到元素全部是0以及两矩阵之间某一个是0的的值  就是减去全部都是1的
    temp = tempdeg - Matrix_similarity
    # 然后就是全部都是1的比上1-（全部都是1的）
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
    fp1 = open('../Json/Jaccard_similar.json', 'w+')
    fp1.write(doc)
    fp1.close()
    EndTime = time.perf_counter()
    print(f"Jaccard Index SimilarityTime: {EndTime - StartTime} s")
    return Matrix_similarity

