# -*-coding:utf-8 -*-
"""
 @author   : sc
 @Function : 爬虫——爬取爱爱医医疗网站病例
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

path = r"G:\医疗病例\爱爱医学"
pathlist = os.listdir(path)
for i in pathlist:
    corepath = path + "\\"+ i
    corepathlist = os.listdir(corepath)
    for j in corepathlist:
        mainpath = corepath+"\\"+j
        fa = open(mainpath+"\\"+j+"病例页数链接.txt", "r", encoding="UTF-8")
        lines = fa.readlines()
        for line in lines:
            wb_data = requests.get(line, timeout=30, headers=random.choice(headers_pool))
            soup = BeautifulSoup(wb_data.text, 'lxml')
            all_dir = soup.select('div.s_2list > ul > li > a.s_a')
            for link in all_dir:
                hreflink = link.get('href')
                fb = open(mainpath+"\\"+j+'病例链接.txt', 'a+', encoding="UTF-8")
                fb.write(hreflink+"\n")
        print(mainpath+"已经写完")
