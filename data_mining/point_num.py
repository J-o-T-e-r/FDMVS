# -*- coding: utf-8 -*- 
# @Time : 2021/7/26 21:04 
# @Author : kzl 
# @File : point_num.py
# @contact: kristinaNFQ@gmail.com
import pandas as pd
import json

data = pd.read_csv('../data/train.csv')

Sort = data['7718'].value_counts()
classCount = Sort.to_dict()

json_num = json.dumps(classCount, indent=1)
with open('point_num.json', 'w') as json_file:
    json_file.write(json_num)