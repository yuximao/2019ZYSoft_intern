# channel使用示例
#coding:utf-8
from bs4 import BeautifulSoup
import requests
import random
import sys
#reload(sys)
import importlib,sys

importlib.reload(sys)
#sys.setdefaultencoding('utf-8')

start_url = 'http://x.cnki.net/KCMS/detail/detail.aspx?dbcode=CDFD&dbname=CDFDLAST2017&filename=1016761145.nh&v=MTUwOTExVDNxVHJXTTFGckNVUkxPZlllWnFGaURoVzd6SVZGMjZHTFMrSDlESXFwRWJQSVI4ZVgxTHV4WVM3RGg='


headers_pool = [{'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3'},
                {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3'},
                {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36'}
                ]

def get_chennel_urls(url):


    wb_data = requests.get(start_url, timeout =30,headers = random.choice(headers_pool))
    wb_data.raise_for_status

    # 进行了手动测试编码，并设置好
    wb_data.encoding = ('utf-8')

    soup = BeautifulSoup(wb_data.text,'html.parser')

    links = soup.select('span #ChDivSummary')

    # for link in links:
    #     page_url = link.get('href')
    #     print(page_url + 'wait/')

    print(links[0])
# get_chennel_urls(start_url)
