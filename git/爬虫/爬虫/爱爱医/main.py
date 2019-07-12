# -*-coding:utf-8 -*-
"""
 @author   : sc
 @Function : 爬虫——爬取爱爱医医疗网站文章链接
"""
from bs4 import BeautifulSoup
import requests
import random
import sys
#reload(sys)
import importlib,sys
import os

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
        src = pathcontent + "\\"+u+"页数链接.txt"
        fa = open(src, 'r', encoding='utf-8')
        lines = fa.readlines()
        for line in lines:
            wb_data = requests.get(line, timeout=30, headers=random.choice(headers_pool))
            # 进行了手动测试编码，并设置好
            wb_data.encoding = ('UTF-8')
            soup = BeautifulSoup(wb_data.text, 'lxml')
            all_dir = soup.select('div.ri > a')
            for link in all_dir:
                page_url = link.get('href')
                fa = open(pathcontent+"\\"+u+"文章集链接.txt", "a+", encoding="UTF-8")
                fa.write(page_url+"\n")


    print(paths+"已经写完")

print("finish")
# print(pathlist)