# -*- coding: utf-8 -*- 
# @Time : 2021/7/27 11:26 
# @Author : kzl 
# @File : AA.py.py
# @contact: kristinaNFQ@gmail.com

import numpy as np
import time
import LianLU
import pandas as pd
import json
import warnings
warnings.filterwarnings("ignore")

data = pd.read_csv('data/train.csv')


def AA(Matrix):
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
    doc = json.dumps(All_dict)
    fp1 = open('Json/AA_similar.json', 'w+')
    fp1.write(doc)
    fp1.close()
    EndTime = time.perf_counter()
    print(f"SimilarityTime: {(EndTime - StartTime)}")
    return Matrix_similarity


a = LianLU.Data_Shape(data)
b = LianLU.MatrixAdjacency0(a, data)
AA(b)
