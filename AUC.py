#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@File    ：AUC.py
@Author  ：wkml4996
@Date    ：2021/7/28 17:52 
"""
import json
import random


def AUC(test_mat,full_mat,sim):
    """
    计算AUC值
    :param test_mat: ndarray（10755*10755），测试集边矩阵
    :param full_mat: ndarray (10755*10755)，测试集+训练集的边矩阵
    :param sim: ndarray（10755*10755），相似度矩阵
    :return:AUC
    """
    score = 0
    for i in range(10000):
        # 生成测试集中的一组边
        while(1):
            E_test = random.sample(range(1, 10755), 2)
            if test_mat[E_test[0],E_test[1]] != 0:
                break
        # 生成不存在的一条边
        while(1):
            E_non = random.sample(range(1, 10755), 2)
            if full_mat[E_non[0],E_non[1]] == 0:
                break
        # 计算AUC的分子
        if sim[E_test[0],E_test[1]] > sim[E_non[0],E_non[1]]:
            score += 1
        elif sim[E_test[0],E_test[1]] == sim[E_non[0],E_non[1]]:
            score += 0.5
        else:
            continue
    else:
        # 计算AUC
        print(score,i+1)
        AUC = score / (i+1)
    return AUC