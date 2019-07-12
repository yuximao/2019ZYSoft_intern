# -*-coding:utf-8 -*-
"""
 @author   : sc
 @Function : 爬虫——爬取爱爱医医疗网站文章，生成作者的csv
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
path = r'G:\汇总\医疗文章\爱爱医学\爱爱医学'
pathlist = os.listdir(path)
for i in pathlist:
    paths = path+"\\"+i  # 'G:\医疗文章\爱爱医学\中医科'
    pathlists = os.listdir(paths)
    k = 0
    for u in pathlists:
        pathcontent = paths +"\\"+u # 'G:\医疗文章\爱爱医学\中医科\中医五官科'
        src = pathcontent + "\\"+u+"作者.txt"
        print(src)
        fa = open(src, 'r', encoding='utf-8')
        lines = fa.readline()
        # linelen = len(line)
        # linelen+=linelen
        lines = eval(lines)
        screenname = []
        skills = []
        briefs = []
        doctortitle = []
        belongke = []
        doctorname = []
        for line in lines:
            start_url = line[2]
            keshi = line[1]
            if len(start_url) == 0:
                screenname.append("")
                skills.append("")
                briefs.append("")
                doctortitle.append("")
                belongke.append("")
                doctorname.append("")
            else:
                wb_data = requests.get(start_url, timeout=30, headers=random.choice(headers_pool))
                # 进行了手动测试编码，并设置好
                soup = BeautifulSoup(wb_data.text, 'lxml')
                wb_data.encoding = ('UTF-8')
                netname = soup.select("div.p_person_medal > a")[0].text
                screenname.append(netname) # 医生匿名
                brief = soup.select("div.p_up_cont > p")[0].text
                brief = brief.strip("\n")
                brief = brief.replace("简介：","")
                briefs.append(brief)
                skill = soup.select("div.p_up_cont > span")[0].text
                skill = skill.strip("\n")
                skill = skill.replace("擅长：", "")
                skills.append(skill)
                doctortitle.append(line[1][1])
                doctorname.append(line[0])
                belongke.append(line[1][0])
        fb = open(pathcontent + "\\" + u + "作者.csv", 'a+', encoding='utf-8')
        dataframe = pd.DataFrame({'医生姓名': doctorname, '隶属科室': belongke, '医生职称': doctortitle, '医生匿名': screenname, '擅长': skills, '简介':briefs})
        dataframe.to_csv(pathcontent + "\\" + u + "作者.csv", index=False, encoding='utf_8_sig')
        print(pathcontent + "已经写完")
    print(paths + "已经写完")


