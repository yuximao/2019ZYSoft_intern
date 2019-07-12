#coding:utf-8
from bs4 import BeautifulSoup
import requests
import random
import sys
#reload(sys)
import importlib,sys

importlib.reload(sys)
#sys.setdefaultencoding('utf-8')

start_url = 'http://www.wanfangdata.com.cn/search/searchList.do?searchType=perio&showType=detail&pageSize=20&searchWord=%E7%96%BE%E7%97%85&isTriggerTag='
fa = open("/Users/28028/Desktop/智业/爬虫示例/万方/医疗翻页链接.txt", 'r', encoding='utf-8')
lines = fa.readlines()


headers_pool = [{'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3'},
                {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3'},
                {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36'}
                ]

def get_chennel_urls(url):

    for line in lines:
        wb_data = requests.get(line, timeout =30,headers = random.choice(headers_pool))


        # 进行了手动测试编码，并设置好
        wb_data.encoding = ('gbk')

        soup = BeautifulSoup(wb_data.text, 'lxml')

        links = soup.select('div.title > a')
        print(links)
        fa = open("/Users/28028/Desktop/智业/爬虫示例/万方/医疗文章集链接.txt", 'a+', encoding='utf-8')
        for link in links:
            page_url = link.get('href')
            print(page_url)
            fa.write(page_url+'\n')
        fa.close()

        print(len(links))
get_chennel_urls(start_url)
