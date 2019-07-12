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

importlib.reload(sys)
#sys.setdefaultencoding('utf-8')

# 打开链接
start_url = 'http://www.iivd.net/search.php?mod=portal&searchid=29&orderby=aid&ascdesc=desc&searchsubmit=yes&page=2'
fa = open(r"G:\医疗文章\小桔灯\以“医疗”为关键字\医疗文章\医疗翻页链接.txt", 'r', encoding='utf-8')
lines = fa.readlines()

#获取headers
headers_pool = [{'User-Agent':'Mozilla/5.0 (Windows NT 6.2) \
                AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3'},
                {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) \
                AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3'},
                {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36'}
                ]

#保存链接
def get_chennel_urls(url):
    """

    :param url: 翻页链接
    :return: 每一页的文章链接
    """
    for line in lines:
        wb_data = requests.get(line, timeout =30,headers = random.choice(headers_pool))


        # 进行了手动测试编码，并设置好
        wb_data.encoding = ('gbk')

        soup = BeautifulSoup(wb_data.text, 'lxml')
        # 获取链接
        links = soup.select('li.pbw > h3 > a')
        fa = open(r"G:\医疗文章\小桔灯\以“医疗”为关键字\医疗文章\医疗文章集链接.txt", 'a+', encoding='utf-8')
        for link in links:
            page_url = link.get('href')
            print(page_url)
            fa.write(page_url+'\n')
        fa.close()  # 关闭文件

        print(len(links))  # 打印结果

# 调用函数
get_chennel_urls(start_url)
