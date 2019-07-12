# -*— coding:utf-8 -*-
"""
 @author   : sc
 @Function : 爬虫——爬取爱爱医医疗网站文章
"""
from requests import session, Request
from bs4 import BeautifulSoup as bs
import os
import random
# 创建session请求对象，保存登录会话请求u
session_req=session()

# 需要传输的参数
postData={
    "username":"scc_123456",
    "password":""
}
# 需要登录的URL
login_url="https://account.iiyi.com/index/login/"
#PreparedRequest请求预处理
req=Request(
    'post',
    login_url,
    data=postData,
    # headers=dict(referer=login_url)
)
prepped=req.prepare()

#将处理的请求参数通过session请求对象发送过去
resp=session_req.send(prepped)

#用BeautifulSoup处理登录之后返回的数据
soup=bs(resp.content,"html.parser")

headers_pool = [{'User-Agent':'Mozilla/5.0 (Windows NT 6.2) \
                AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3'},
                {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) \
                AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3'},
                {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36'}
                ]
path = r"G:\医疗病例\爱爱医学"
pathlist = os.listdir(path)
for i in pathlist:
    corepath = path + "\\"+ i
    corepathlist = os.listdir(corepath)
    for j in corepathlist:
        mainpath = corepath+"\\"+j
        fa = open(mainpath+"\\"+j+"病例链接.txt", "r", encoding="UTF-8")
        lines = fa.readlines()
        for line in lines:
            wb_data = session_req.get(line, timeout=200, headers=random.choice(headers_pool))
            soup = bs(wb_data.text, 'lxml')
            all_dir = soup.select('div.s_floor21 > p')[0].text
            title = soup.select("div.s_floor1 > h1")[0].text
            all_dir = all_dir.strip("")
            all_dir = all_dir.strip("\r\t\n")
            all_dir = all_dir.split("【")
            del all_dir[0]
            titles = [['文章标题',title]]
            introduction = soup.select("div.s_p2")
            for k in range(len(introduction)):
                everystr = introduction[k].text
                everystr = everystr.lstrip("")
                everystr = everystr.replace("　　","")
                everystr = everystr.strip("\r\t\n")
                everystr = everystr.split("：")
                titles.append(everystr)
            for u in all_dir:
                k = u.split("】")
                titles.append(k)
            dicts = {}
            for ti in titles:
                # print(len(ti))
                if(len(ti)) != 2:
                    titles.pop(titles.index(ti))
                else:
                    dicts[ti[0]] = ti[1]
            fb = open(mainpath + "\\" + j + '新病例1.txt', 'a+', encoding="UTF-8")
            fb.write(str(dicts)+"\n")
        print(mainpath+"已经写完")