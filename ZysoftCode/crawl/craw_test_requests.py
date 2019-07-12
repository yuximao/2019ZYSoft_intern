# requests使用示例
# -*- coding:UTF-8 -*-

from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
if __name__ == "__main__":
     target = 'http://www.wanfangdata.com.cn/details/detail.do?_type=perio&id=zjyfyx201904011#'
     req = requests.get(url = target)
     html = req.text
     bs = BeautifulSoup(html,"html.parser")

     texts = bs.find_all('div',id='see_alldiv')
     print(texts[0].text.replace('\xa0'*8,'\n\n'))

     # print(texts)
     # for a in bs.find_all('a',class_ = 'fz14', href=True):
     #      print("Found the URL:", a['href'])



     # f = open('testfile.txt', 'w+')
     # for j in range(len(texts)):
     #      f.write(str(texts[j]).replace('\xa0','') )
     # f.close()
     # pd.DataFrame({'text':texts[0].text.replace('\xa0'*8,'\n\n')}).to_csv("testfile.csv",encoding='gb18030')

