#coding:utf-8
from bs4 import BeautifulSoup
import requests
import random
import sys
import os
#reload(sys)
import importlib,sys
import pandas as pd
importlib.reload(sys)
import re
#sys.setdefaultencoding('utf-8')
web_bef = 'http://www.iivd.net/article-16035-1.html'
headers_pool = [{'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3'},
                {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3'},
                {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36'}
                ]

wb_data = requests.get(web_bef, timeout=30, headers=random.choice(headers_pool))
wb_data.encoding = ('gbk')
soup = BeautifulSoup(wb_data.text, 'lxml')
title = soup.select('h1')[0].text
print(type(title))
date = soup.select('p[class="xg1"]')[0].text
date = date.replace('\r\n', '')
date = '日期: '+date
date = date.replace('|', ': ')
date = date.split(': ')
data = []
for i in date:
    if date.index(i)%2 != 0:
        data.append(i)
print(date)
print(data)

article = soup.select('td[id="article_content"]')[0].text
print(article)
# fb = open("G:\医疗文章\小桔灯\诊疗指南\诊疗指南文章\诊疗指南文章.csv", 'a+', encoding='utf-8')
# # dataframe = pd.DataFrame({'文章标题':title, '日期':})