# -*-coding:utf-8 -*-
"""
 @author   : sc
 @Function : 爬虫——爬取爱爱医医疗网站文章，获取作者的txt文件
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
path = r'G:\汇总\医疗文章\爱爱医学\爱爱医学'
pathlist = os.listdir(path)
for i in pathlist:
    paths = path+"\\"+i  # 'G:\医疗文章\爱爱医学\中医科'
    pathlists = os.listdir(paths)
    for u in pathlists:
        pathcontent = paths +"\\"+u # 'G:\医疗文章\爱爱医学\中医科\中医五官科'
        src = pathcontent + "\\"+u+"文章集链接.txt"
        fa = open(src, 'r', encoding='utf-8')
        lines = fa.readlines()
        links = []
        ke = []
        aut = []
        alllist = []
        for line in lines:
            wb_data = requests.get(line, timeout=30, headers=random.choice(headers_pool))
            # 进行了手动测试编码，并设置好
            soup = BeautifulSoup(wb_data.text, 'lxml')
            wb_data.encoding = ('UTF-8')
            keshizhicheng = soup.select("div.info > em")
            all_dir = soup.select('div.info > var > a')
            if len(all_dir) == 0:
                links.append("")
                aut.append("爱爱医")
            else:
                dir = all_dir[0]
                author = all_dir[0].text
                link = dir.get("href")
                links.append(link)
                aut.append(author)
            if len(keshizhicheng) == 0:
                ke.append(keshizhicheng)
            else:
                keshizhicheng = soup.select("div.info > em")[0].text
                kezhi = keshizhicheng.split("|")
                ke.append(kezhi)
        alllist = list(zip(aut,ke,links))
        fb = open(pathcontent+"\\"+u+"作者.txt", 'a+', encoding='utf-8')
        fb.write(str(alllist))
        fb.close()
        print(pathcontent+"已经写完")
