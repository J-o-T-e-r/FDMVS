import re
import json
import numpy as np
import pandas as pd

#读取全部数据
origin_data = {}
for i in range(1, 10755):
    origin_data[i] = pd.read_csv('%d.txt' % i, header=None).values.tolist()

#统计每个词的出现的次数
words_num = {}
for key in origin_data.keys():
    temp_list = origin_data[key]
    for item in temp_list:
        if item[0] not in words_num.keys():
            words_num[item[0]] = 0
        words_num[item[0]] += 1
#出现次数从多到少进行排序
words_num = list(sorted(words_num.items(), key=lambda x: x[1], reverse=True))

#统计大学出现的次数
universities = []
for i in range(len(words_num)):
    if re.findall("(.*大学)", str(words_num[i][0])):
        universities.append(re.findall("(.*大学)", str(words_num[i][0]))[0])
universities = list(set(universities))
#人为手工剔除脏数据
universities.remove('大学')
universities.remove('理工大学')
#创建字典，key:大学的名称 values：出现的次数
colleges = {}
for i in range(len(words_num)):
    for university in universities:
        if words_num[i][0] == university:
            colleges[words_num[i][0]] = words_num[i][1]
#写入json文件（大学出现次数get）
# university = json.dumps(colleges, ensure_ascii = False)
# fp1 = open('university.json', 'w+')
# fp1.write(university)
# fp1.close()


#从原始数据中提取每个学者的研究兴趣
#从研究兴趣的下一个开始提取，直到experience
interest = {}
for key in origin_data.keys():
    temp_interest = []
    temp_list = origin_data[key]
    for i in range(len(temp_list)):
        if temp_list[i][0] == '研究兴趣':
            for j in range(i + 1, len(temp_list)):
                if temp_list[j][0] == 'experience':
                    break
                temp_interest.append(temp_list[j])
            break
    interest[key] = temp_interest
#删去研究兴趣很长的用户
for key in interest.keys():
    temp_list = interest[key]
    if len(temp_list) > 5:
        interest[key] = []
#改变一下格式，存为字典，key:id, values:研究兴趣
interests = {}
for key in interest.keys():
    t_list = []
    temp_list = interest[key]
    for temp in temp_list:
        t_list.append(temp[0])
    interests[key] = t_list
#写入json文件（每个id的研究兴趣get）
# interests = json.dumps(interests, ensure_ascii = False)
# fp1 = open('interests.json', 'w+')
# fp1.write(interests)
# fp1.close()


#统计研究兴趣出现的次数
interest_words = {}
for key in interest.keys():
    temp_list = interest[key]
    for temp in temp_list:
        if temp[0] not in interest_words.keys():
            interest_words[temp[0]] = 0
        interest_words[temp[0]] += 1
#从大到小排序
interest_rank = sorted(interest_words.items(),key = lambda x:x[1],reverse = True)
#人为去除一些奇怪的东西
stop_words = ['技术', '工程', 'javabiographyintroductioneducationwork', '学生', '基础', '学习', 'itbiographyintroductioneducationwork']
interests_rank = {}
for item in interest_rank:
    if item[0] not in stop_words:
        interests_rank[item[0]] = item[1]
# 写入json文件（研究兴趣热门榜单get）
# interests_rank = json.dumps(interests_rank, ensure_ascii = False)
# fp1 = open('interests_rank.json', 'w+')
# fp1.write(interests_rank)
# fp1.close()

#字典，keys:研究兴趣， values:id
interests_id = {}
for key in interests.keys():
    temp_list = interests[key]
    for item in temp_list:
        if item not in interests_id.keys():
            interests_id[item] = []
        interests_id[item].append(key)
# 写入json文件（每个研究兴趣及对它感兴趣的学者数据get）
# interests_id = json.dumps(interests_id, ensure_ascii = False)
# fp1 = open('interests_id.json', 'w+')
# fp1.write(interests_id)
# fp1.close()

#提取教育水平
education = ['本科', '本科生', '硕士', '博士', '博士后', '硕士生', '研究生', '硕士学位', '大学生', '学士', '学士学位', '博士生']
education_temp = []
for word in words_num:
    if word[0] in education:
        education_temp.append(word)
#去重
#keys:教育水平 values:人数
educations = {}
educations['本科'] = 0
educations['硕士'] = 0
educations['博士'] = 0
educations['博士后'] = 0
for temp in education_temp:
    if (temp[0] == '本科') | (temp[0] == '大学生') | (temp[0] == '学士') | (temp[0] == '学士学位') | (temp[0] == '本科生'):
        educations['本科'] += int(temp[1])
    if (temp[0] == '硕士') | (temp[0] == '研究生') | (temp[0] == '硕士学位') | (temp[0] == '硕士生'):
        educations['硕士'] += int(temp[1])
    if (temp[0] == '博士') | (temp[0] == '博士生'):
        educations['博士'] += int(temp[1])
    if (temp[0] == '博士后'):
        educations['博士后'] += int(temp[1])
#写入json文件（大致教育水平get）
# educations = json.dumps(educations, ensure_ascii = False)
# fp1 = open('educations.json', 'w+')
# fp1.write(educations)
# fp1.close()

#统计词云图所需数据
total = 0
for key in interests_rank.keys():
    total += interests_rank[key]
wordcloud = {}
for key in interests_rank.keys():
    wordcloud[key] = interests_rank[key] / total
wordcloud = pd.DataFrame(wordcloud, index=['频率'])
#存入表格
#wordcloud.to_excel('wordcloud.xlsx')