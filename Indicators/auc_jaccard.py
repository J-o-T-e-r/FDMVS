# -*- coding: utf-8 -*- 
# Time : 2021/7/29 22:38
# Author : Kristina
# File : CN.py
# contact: kristinaNFQ@163.com
# MyBlog: kristina100.github.io
# -*- coding:UTF-8 -*-

"""
@File    ：AUC.py
@Author  ：wkml4996
@Date    ：2021/7/28 17:52
"""

import random

def AUC(test_mat, full_mat, sim):
    """
    计算AUC值
    :param test_mat: ndarray（10755*10755），测试集边矩阵
    :param full_mat: ndarray (10755*10755)，测试集+训练集的边矩阵
    :param sim: ndarray（10755*10755），相似度矩阵
    :return:AUC
    """
    global i
    score = 0
    for i in range(10000):
        while 1:
            E_test = random.sample(range(1, 10755), 2)
            if test_mat[E_test[0], E_test[1]] != 0:
                break
        while 1:
            E_non = random.sample(range(1, 10755), 2)
            if full_mat[E_non[0], E_non[1]] == 0:
                break
        if sim[E_test[0], E_test[1]] > sim[E_non[0], E_non[1]]:
            score += 1
        elif sim[E_test[0], E_test[1]] == sim[E_non[0], E_non[1]]:
            score += 0.5
        else:
            continue
    else:
        AUC = score / (i + 1)
        print(f"AUC:{AUC}\n")
    return AUC