# -*-coding:utf-8 -*-
"""
 @author   : sc
 @Function : 爬虫——爬取爱爱医医疗网站文章，爬取文章链接
"""
from bs4 import BeautifulSoup
import requests
import random
import sys
#reload(sys)
import importlib,sys
import os

importlib.reload(sys)
#sys.setdefaultencoding('utf-8')

start_url = 'https://article.iiyi.com/'


headers_pool = [{'User-Agent':'Mozilla/5.0 (Windows NT 6.2) \
                AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3'},
                {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) \
                AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3'},
                {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36'}
                ]

wb_data = requests.get(start_url, timeout =30,headers = random.choice(headers_pool))


# 进行了手动测试编码，并设置好
wb_data.encoding = ('UTF-8')

soup = BeautifulSoup(wb_data.text, 'lxml')

all_dir = soup.select('div.left_menu > ul > li')
all_dir_href = soup.select('div.left_menu > ul > li > a')

dirhref = [] # 疾病网址集合
for link in all_dir_href:
    href = link.get('href')
    dirhref.append(href)
print(dirhref)

dirarr = [] # 各种疾病名称
for dir in all_dir:
    dircontent = dir.text
    dirhref = dir.get('href')
    dirarr.append(dircontent)

print(dirarr)

la = ['https://article.iiyi.com/', 'https://article.iiyi.com/hot/1-999.html', 
		'https://article.iiyi.com/hot/1-1.html', 'https://article.iiyi.com/hot/1-2.html', 
		'https://article.iiyi.com/hot/1-3.html', 'https://article.iiyi.com/hot/1-4.html', 
		'https://article.iiyi.com/hot/1-6.html', 'https://article.iiyi.com/hot/1-7.html',
		'https://article.iiyi.com/hot/1-9.html', 'https://article.iiyi.com/hot/1-10.html', 
		'https://article.iiyi.com/hot/1-11.html', 'https://article.iiyi.com/hot/1-13.html', 
		'https://article.iiyi.com/hot/1-14.html', 'https://article.iiyi.com/hot/1-15.html', 
		'https://article.iiyi.com/hot/1-544.html', 'https://article.iiyi.com/hot/1-545.html',
		'https://article.iiyi.com/hot/1-542.html', 'https://article.iiyi.com/hot/1-18.html']
lb = ['最新', '推荐', '内科', '外科', '儿科', '传染病科', '妇产科', '精神心理科', 
		'皮肤性病科', '中医科', '肿瘤科', '骨科', '康复医学科', '麻醉医学科', '医技科', 
		'医学影像学', '五官科', '其他科室']
me = dict(zip(lb,la))
print(me)
