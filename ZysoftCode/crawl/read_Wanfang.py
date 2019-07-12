#根据已有的摘要连接，下载摘要
from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
import time
import re
fa = open("/Users/28028/Desktop/智业/爬虫示例/万方/医疗文章集链接.txt", 'r', encoding='utf-8')
lines = fa.readlines()
# fb = open("/Users/28028/Desktop/智业/爬虫示例/万方/医疗文章.csv", '', encoding='utf-8')
abstr=[]
title=[]
author=[]
orgn=[]
paper=[]
doi=[]
keyw=[]
url=[]
pubnum=[]
pubdate=[]
themes=[]
theme='病例报告'
i=0
for line in lines:
    try:
        time.sleep(2)
        target = line
        req = requests.get(url=target)
        html = req.text
        bs = BeautifulSoup(html, "html.parser")
        # 摘要
        # aa=''
        try:
            texts = bs.find_all('div', class_='abstract')
            aa = texts[0].find('textarea').text.replace('\xa0' * 8, '\n\n')
            abstr.append(aa)
        except:
            abstr.append(' ')

        # 标题
        # tit=''
        try:
            texts2 = bs.find_all('font', style='font-weight:bold;')
            tit=texts2[0].text.replace('\xa0' * 8,'\n\n')
            title.append(tit)
        except:
            tit=line
            title.append(' ')
        # 作者
        try:
            texts3=bs.find_all('a', class_='info_right_name')
            author.append(texts3[0].text.replace('\xa0' * 8,'\n\n'))
        except:
            author.append(' ')
        # 组织
        try:
            texts4=bs.find_all('a', id='unit_nameType5')
            orgn.append(texts4[0].text.replace('\xa0' * 8, '\n\n'))
        except:
            orgn.append(' ')
        # 发表处
        try:
            texts5 = bs.find_all('a', class_='college')
            paper.append(texts5[0].text.replace('\xa0' * 8, '\n\n',))
        except:
            paper.append(' ')
        # 关键词
        try:
            texts7 = bs.find_all('div', class_='info_right info_right_newline')
            keyw.append(texts7[0].text.replace('\xa0' * 8, '',))
        except:
            keyw.append(' ')
        # url
        url.append(line)
        # 日期
        try:
            pubdate.append(bs.find_all('div', string=re.compile('.*年.*月'))[0].text.replace('\xa0' * 8, '',))
        except:
            pubdate.append(' ')
        # 杂志号
        try:
            pubnum.append(bs.find_all('div', string=re.compile('20.*,.*\('))[0].text.replace('\xa0' * 8, '',))
        except:
            pubnum.append(' ')
        # doi
        try:
            doi.append(bs.find_all('a', string=re.compile('.*\..*\/'))[0].text.replace('\xa0' * 8, '\n\n',))
        except:
            doi.append(' ')
        themes.append(theme)
        # print(abstr)
        # print('title',title)
        # print('author',author)
        # print('orgn',orgn)
        # print('paper',paper)
        # print('关键词',keyw)
        i=i+1
        dataframe = pd.DataFrame(
            {'主题':themes,'标题': title,'链接':url ,'关键词':keyw,'作者': author, '机构': orgn,'来源': paper, '出版日期':pubdate,'出版编号':pubnum,'doi':doi,'文章摘要': abstr})
        dataframe.to_csv("/Users/28028/Desktop/智业/爬虫示例/万方/医疗文章.csv", index=False, encoding='utf_8_sig')
        fobj = open('/Users/28028/Desktop/智业/爬虫示例/万方/txt/' + tit + '.txt', 'w', encoding='utf-8')
        fobj.write(aa)
        fobj.close()
        print(i,'成功')
        print('-----------------------------------------')
    except:
        print('失败！！-----------------------------------------------')