#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    ：precision.py
@Author  ：wkml4996
@Date    ：2021/7/29 15:29 
"""
from collections import Counter
import numpy as np


def prescision(mat,test_mat,sim_,):
    """
    计算prescision
    :param mat: ndarray（10755*10755），训练集矩阵
    :param test_mat: ndarray (10755*10755)，测试集矩阵
    :param sim_: ndarray（10755*10755），相似度矩阵
    :return: Pr 精确度
    """
    max_list = []
    for i in range(mat.shape[0]):
        max_list.append(np.sort(sim_[i])[::-1][1])
    mean = np.mean(max_list)
    # 比较的次数
    L = 1000
    # 所有相似度的排序列表
    L_list = {}
    for v1 in range(sim_.shape[0]):
        # 这一步是记录下排序之后的值和索引，
        sim_sort = np.sort(sim_[v1])[::-1][1:]
        _v2 = np.argsort(sim_[v1])[::-1][1:]
        for sim, v2 in zip(sim_sort, _v2):
            # 先取一次平均
            if sim > mean:
                L_list[(v1, v2)] = sim
                # 一直加列表到一千位
                if len(L_list) < L:
                    continue
                else:
                    # 将相似度列表排序，不断筛出前一千个最大的相似度
                    re = Counter(L_list).most_common(L)
                    L_list = {}
                    for k, v in re:
                        L_list[k] = v
            else:
                break

    """
    相似度排序列表的样子大概是下面这样：
    键：两个结点，值：相似度
    L_list = {(1,2) = 999
              (2,1) = 998
              (3,99) = 991
              ...

    }
    """
    score = 0
    for v1, v2 in L_list.keys():
        if test_mat[v1][v2] == 1:
            score += 1
    Pr = score / L
    return Pr