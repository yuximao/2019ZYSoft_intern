# -*-coding:utf-8 -*-
"""
 @author   : sc
 @Function : 爬虫——爬取爱爱医医疗网站文章，爬取核心内容
"""
from bs4 import BeautifulSoup
import requests
import random
import sys
#reload(sys)
import importlib,sys
import os
import pandas as pd
importlib.reload(sys)
headers_pool = [{'User-Agent':'Mozilla/5.0 (Windows NT 6.2) \
                AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3'},
                {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) \
                AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3'},
                {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36'}
                ]
path = r'G:\医疗文章\爱爱医学'
pathlist = os.listdir(path)
for i in pathlist:
    paths = path+"\\"+i  # 'G:\医疗文章\爱爱医学\中医科'
    pathlists = os.listdir(paths)
    for u in pathlists:
        pathcontent = paths +"\\"+u # 'G:\医疗文章\爱爱医学\中医科\中医五官科'
        src = pathcontent + "\\"+u+"文章集链接.txt"
        fa = open(src, 'r', encoding='utf-8')
        lines = fa.readlines()
        titlearr = []
        abstracttarr = []
        datearr = []
        readtimes = []
        articlearr = []
        for line in lines:
            wb_data = requests.get(line, timeout=30, headers=random.choice(headers_pool))
            # 进行了手动测试编码，并设置好
            wb_data.encoding = ('UTF-8')
            soup = BeautifulSoup(wb_data.text, 'lxml')
            title = soup.select('h1')[0].text
            titlearr.append(title)
            abstract = soup.select("div.cont > span.sp")[0].text
            abstracttarr.append(abstract)
            article = soup.select('div.cont p')
            articles = ['']
            for i in range(len(article)):
                article[i] = article[i].text
                articles[0] += article[i]

            articlearr.append(articles)

            temp = soup.select("div.top > span > var")[0].text
            temp = temp.split("　　")
            datearr.append(temp[0])
            readtimes.append(temp[1])
        fb = open(pathcontent+"\\"+u+".csv", 'a+', encoding='utf-8')
        dataframe = pd.DataFrame({'文章标题': titlearr, '日期': datearr,  '浏览次数': readtimes,  '文章内容': articlearr, '导读':abstracttarr})
        dataframe.to_csv(pathcontent+"\\"+u+".csv", index=False, encoding='utf_8_sig')
        print(pathcontent + "已经写完")
    print(paths+"已经写完")