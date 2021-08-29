# -*- coding: utf-8 -*- 
# @Time : 2021/7/26 17:37 
# @Author : kzl 
# @File : dataMining.py
# @contact: kristinaNFQ@gmail.com

import re
import json


def dataParse(bigString):
    listOfTokens = re.split(r'\W+', bigString)
    if len(listOfTokens) > 1:
        return listOfTokens


def readTxt():
    # 创建一个字典
    docDict = {}
    for i in range(1, 10755):
        # 读取单个txt文件
        wordList = dataParse(open(f"attribute/{i}.txt", 'r', encoding='UTF-8').read())
        # 遍历列表，留下id和研究兴趣 后面的字段
        if wordList[0] == '研究兴趣':
            List = []
            try:
                for j in range(1, 3):
                    List.append(wordList[j])
            except Exception:
                continue
            docDict[i] = List
        json_str = json.dumps(docDict, ensure_ascii=False, indent=1)
        with open('YanJiuXingQu.json', 'w', encoding="utf-8") as json_file:
            json_file.write(json_str)


readTxt()
