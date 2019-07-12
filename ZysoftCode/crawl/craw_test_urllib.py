# 普通的网页爬虫演示
# import urllib.request
# url = "http://www.douban.com/"
# webPage=urllib.request.urlopen(url)
# data = webPage.read()
# data = data.decode('UTF-8')
# print(data)
# print(type(webPage))
# print(webPage.geturl())
# print(webPage.info())
# print(webPage.getcode())

# 伪装成浏览器的爬虫
# import urllib.request
# weburl = "http://www.douban.com/"
# webheader = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
# req = urllib.request.Request(url=weburl, headers=webheader)
# webPage=urllib.request.urlopen(req)
# data = webPage.read()
# data = data.decode('UTF-8')
# print(data)
# print(type(webPage))
# print(webPage.geturl())
# print(webPage.info())
# print(webPage.getcode())

# 复杂示例
# import urllib.request
# weburl = "http://www.douban.com/"
# webheader1 = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
# webheader2 = {
#     'Connection': 'Keep-Alive',
#     'Accept': 'text/html, application/xhtml+xml, */*',
#     'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
#     #'Accept-Encoding': 'gzip, deflate',
#     'Host': 'www.douban.com',
#     'DNT': '1'
#     }
# req = urllib.request.Request(url=weburl, headers=webheader2)
# webPage=urllib.request.urlopen(req)
# data = webPage.read()
# data = data.decode('UTF-8')
# print(data)
# print(type(webPage))
# print(webPage.geturl())
# print(webPage.info())
# print(webPage.getcode())

# 爬图片 -失败了
import urllib.request
import socket
import re
import sys
import os
targetDir = r"C:\Users\28028\Desktop\智业\爬虫示例"  #文件保存路径
def destFile(path):
    if not os.path.isdir(targetDir):
        os.mkdir(targetDir)
    pos = path.rindex('/')
    t = os.path.join(targetDir, path[pos+1:])
    return t
if __name__ == "__main__":  #程序执行入口
    weburl = "https://www.iivd.net/article-17506-1.html"
    webheaders = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib.request.Request(url=weburl, headers=webheaders)  #构造请求报头
    webpage = urllib.request.urlopen(req)  #发送请求报头
    contentBytes = webpage.read()
    print(contentBytes)
    print(type(webpage))
    print(webpage.geturl())
    print(webpage.info())
    print(webpage.getcode())
    for link, t in set(re.findall(r'(https:[^\s]*(jpg|png|gif))', str(contentBytes))): #正則表達式查找全部的图片

        print(link)
        try:
            urllib.request.urlretrieve(link, destFile(link)) #下载图片
            print('sucess!')
        except:
            print('失败') #异常抛出

# 爬整个网页内容
# import urllib.request
# def saveFile(data):
#     save_path = 'D:\\temp.out'
#     f_obj = open(save_path, 'wb') # wb 表示打开方式
#     f_obj.write(data)
#     f_obj.close()
# weburl = "http://www.douban.com/"
# webheader1 = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
# webheader2 = {
#     'Connection': 'Keep-Alive',
#     'Accept': 'text/html, application/xhtml+xml, */*',
#     'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
#     #'Accept-Encoding': 'gzip, deflate',
#     'Host': 'www.douban.com',
#     'DNT': '1'
#     }
# req = urllib.request.Request(url=weburl, headers=webheader2)
# webPage=urllib.request.urlopen(req)
# data = webPage.read()
# saveFile(data)# 将data变量保存到 D 盘下
# data = data.decode('UTF-8')
# print(data)
# print(type(webPage))
# print(webPage.geturl())
# print(webPage.info())
# print(webPage.getcode())

