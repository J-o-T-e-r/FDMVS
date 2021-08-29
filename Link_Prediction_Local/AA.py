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


def AA(Matrix):
    """

    :param Matrix: 邻接矩阵
    :return: 返回相似度矩阵
             对预测边按照相似度大小进行排序
    """
    StartTime = time.perf_counter()
    log = np.log(sum(Matrix))
    log = np.nan_to_num(log)
    log.shape = (log.shape[0], 1)
    Matrix_Log = Matrix / log
    Matrix_Log = np.nan_to_num(Matrix_Log)
    Matrix_similarity = np.dot(Matrix, Matrix_Log)
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
        List = sorted(List.items(), key=lambda item: (item[1], item[0]), reverse=True)
        All_dict[i] = List
        Dict = {}
        Dict[i] = All_dict[i]

        doc = json.dumps(Dict)
        fp1 = open('../Json/A0_similar.json', 'a')
        fp1.write(doc)

    EndTime = time.perf_counter()
    print(f"Adamic–Adar Index similarityTime: {(EndTime - StartTime)}")
    return Matrix_similarity

