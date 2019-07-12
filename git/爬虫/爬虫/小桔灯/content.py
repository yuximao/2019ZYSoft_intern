#coding:utf-8
"""
 @author   : sc
 @Time     : 2019/6/3;
 @Function : 爬虫——爬取小桔灯网以“病例报告”、“诊疗指南”、“临床研究”，“系统评价”为搜索关键词的文章
"""
from bs4 import BeautifulSoup
import requests
import random
import importlib,sys
import pandas as pd
importlib.reload(sys)
#sys.setdefaultencoding('utf-8')
web_bef = 'http://www.iivd.net/'




headers_pool = [{'User-Agent':'Mozilla/5.0 (Windows NT 6.2) \
                AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3'},
                {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) \
                AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3'},
                {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36'}
                ]
fa = open(r"G:\医疗文章\小桔灯\以“医疗”为关键字\医疗文章\医疗文章集链接.txt", 'r', encoding='utf-8')
lines = fa.readlines()
fb = open(r"G:\医疗文章\小桔灯\以“医疗”为关键字\医疗文章\医疗文章.csv", 'a+', encoding='utf-8')

titlearr = []
datearr = []
editarr = []
checkcountarr = []
commentcountarr = []
sourcearr = []
articlearr = []
for line in lines:
    start_url = web_bef+line
    start_url = start_url.strip('\n')
    # print(start_url)
    wb_data = requests.get(start_url, timeout=60, headers=random.choice(headers_pool))
    wb_data.encoding = ('gbk')
    soup = BeautifulSoup(wb_data.text, 'lxml')
    title = soup.select('h1')[0].text
    # print(type(title))
    titlearr.append(title)
    date = soup.select('p[class="xg1"]')[0].text
    date = date.replace('\r\n', '')
    date = '日期: ' + date
    date = date.replace('|', ': ')
    date = date.split(': ')
    data = []
    for i in date:
        if date.index(i) % 2 != 0:
            data.append(i)
    datearr.append(data[0])
    editarr.append(data[1])
    checkcountarr.append(data[2])
    commentcountarr.append(data[3])
    sourcearr.append(data[4])
    article = soup.select('td[id="article_content"]')[0].text
    articlearr.append(article)

print(len(titlearr))
print(len(editarr))
print(len(datearr))
print(len(checkcountarr))
print(len(commentcountarr))
print(len(sourcearr))
print(len(articlearr))
fb = open(r"G:\医疗文章\小桔灯\以“医疗”为关键字\医疗文章\医疗文章.csv", 'a+', encoding='utf-8')
dataframe = pd.DataFrame({'文章标题':titlearr, '日期':datearr, '编辑人员':editarr, '查看次数':checkcountarr,
                          '评论次数':commentcountarr, '来源':sourcearr, '文章内容':articlearr})
dataframe.to_csv(r"G:\医疗文章\小桔灯\以“医疗”为关键字\医疗文章\医疗文章.csv", index=False, encoding='utf_8_sig')
