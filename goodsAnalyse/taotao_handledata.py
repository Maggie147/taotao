# coding: utf-8
# python3.5
__author__ = 'green'

import re
import time
import requests
import pandas as pd
from retrying import retry
from concurrent.futures import ThreadPoolExecutor
import missingno as msno

datatmsp = pd.read_excel('datatmsp.xls')
msno.bar(datatmsp.sample(len(datatmsp)), figsize=(10,4))

half_count = len(datatmsp)/2
datatmsp = datatmsp.dropna(thresh = half_count, axis=1)


datatmsp = datatmsp.drop_duplicates()

# 取这4列数据
data = datatmsp[['item_loc', 'raw_title', 'view_price', 'view_sales']]

# 默认查看前5行的数据
# data.head()


# 对 item_loc列的省份和城市进行拆分
# data.loc[:, 'province']  = data.item_loc.apply(lambda x: str(x).split()[0])
data.loc[:, 'province'] = data.loc[:, 'item_loc'].apply(lambda x: str(x).split()[0])

# # 注： 因为直辖市的省份和城市相同，简单的根据字符长度进行判断
data.loc[:, 'city'] = data.loc[:, 'item_loc'].apply(lambda  x: str(x).split()[0] if len(str(x)) < 4 else str(x).split()[1])

# 提取 view_sales 列中的数字， 得到sales列
data.loc[:, 'sales'] = data.loc[: , 'view_sales'].apply(
					lambda x: str(x).split('人')[0])

# 查看各列的数据类型
data.dtypes

# 将数据类型进行转换
data.loc[:,'sales'] = data.loc[:,'sales'].astype('int')


list_col = ['province', 'city']
for i in list_col:
	data.loc[:, i] = data.loc[:, i].astype('category')

# 删除不用的列
data = data.drop(['item_loc', 'view_sales'], axis=1)

print(data.loc[:].head())

#################################
# 对 raw_title 列标题进行文本分析
title = data.loc[:, 'raw_title'].tolist()
# print(type(title))

import jieba
title_s = []
for line in title:
	title_cut = jieba.lcut(line)      # 对每个标题进行分词
	title_s.append(title_cut)

# 剔除停词
import codecs
stopwords = [line.strip()  for line in codecs.open('./stopwords.txt', 'r', 'utf-8').readlines() if line]
print(type(stopwords))

title_clean = []
for line in title_s:
	line_clean = []
	for word in line:
		if word not in stopwords:
			line_clean.append(word)
	title_clean.append(line_clean)


# 进行去重
title_clean_dist = []
for line in title_clean:
	line_dist = []
	for word in line:
		if word not in line_dist:
			line_dist.append(word)

	title_clean_dist.append(line_dist)

# 将 title_clean_dist 转化为一个list: allwords_clean_dist
allwords_clean_dist = []
for line in title_clean_dist:
	for word in line:
		allwords_clean_dist.append(word)

df_allwords_clean_dist = pd.DataFrame(
							{'allwords': allwords_clean_dist})

word_count = df_allwords_clean_dist.allwords.value_counts().reset_index()
# word_count.colums = ['word', 'count']


print(type(word_count))
word_count['word'] = None
word_count['count'] = None


# 词云可视化
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from scipy.misc import imread

plt.figure(figsize=(20,10))

pic = imread("shafa.png")
w_c = WordCloud(font_path = "./data/simhei.ttf",
				background_color = "white",
				mask = pic, max_font_size=60, margin=1)

wc = w_c.fit_words({
	x[0]:x[1] for x in word_count.head(100).values
	})

plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.show()
