# 自动下载知网的摘要信息
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import pandas as pd
import re
from datetime import datetime

# 实验成功！ 爬取知网论文摘要：
theme='系统评价'
themes=[]
abs = []
titles = []
author = []
orgn = []
paper = []
url = []
pubtime=[]
paperdate=[]
issn=[]
gjc=[]
# 写入文件
def write_to_file(title,zhaiyao):
    # 打开文件
    fobj=open('/Users/28028/Desktop/智业/爬虫示例/知网/'+title+'.txt','w',encoding='utf-8')
    fobj.write(zhaiyao)
    fobj.close()
# 检察元素
def isPresent(browser,self):
    # 检查id查找的内容
    try:
        browser.find_element_by_id(self)
    except :
        return False
    return True
def isPresentbyclass(browser,self):
    # 判断class查找的内容
    try:
        browser.find_element_by_class_name(self)
    except :
        return False
    return True
def isPresentbypath(browser,self):
    # 判断path查找的内容
    try:
        browser.find_element_by_xpath(self)
    except :
        return False
    return True
# 自动翻页
def switchNextPage(page,browser):
    # 自动翻页
    browser.switch_to_frame("iframeResult")
    time.sleep(1)
    #browser.find_element_by_link_text('下一页').click()
    if page==1:
        browser.find_element_by_xpath('//*[@id="ctl00"]/table/tbody/tr[3]/td/table/tbody/tr/td/div/a[9]').click()
    else:
        browser.find_element_by_xpath('//*[@id="ctl00"]/table/tbody/tr[3]/td/table/tbody/tr/td/div/a[11]').click()
    time.sleep(8)
    all_handles = browser.window_handles#获取所有窗口句柄
    for handle in all_handles:#始终获得当前最后的窗口，所以要多次使用
            browser.switch_to_window(handle)

# 下载摘要
def get_abstract(page, browser):
    # 下载摘要内容
    now_handle = browser.current_window_handle

    for i in range(0, 50):  # 每页二十篇论文
        if (abs):
            browser.switch_to_frame("iframeResult")

        time.sleep(3)
        ii = str(i + 2)
        tim=''

        if isPresentbypath(browser, '//*[@id="ctl00"]/table/tbody/tr[2]/td/table/tbody/tr[' + ii + ']/td[5]'):
            tim = browser.find_element_by_xpath(
                '//*[@id="ctl00"]/table/tbody/tr[2]/td/table/tbody/tr[' + ii + ']/td[5]').text
        else:
            tim='null'

        browser.find_elements_by_class_name('fz14')[i].click()
        # browser.find_elements_by_xpath('//*[@id="ctl00"]/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/a').click()
        all_handles = browser.window_handles  # 获取所有窗口句柄
        for handle in all_handles:  # 始终获得当前最后的窗口，所以要多次使用
            browser.switch_to_window(handle)
        # 获取论文题目-titles
        if isPresent(browser, 'ChDivSummary'):
            if (isPresentbypath(browser,'//*[contains(.,"关键词：")]')):
                if (isPresentbypath(browser, '//*[contains(.,"基金：")]')):
                    a = browser.find_element_by_xpath('//*[@class="wxBaseinfo"]/p[3]').text
                    print(a)
                    gjc.append(a)
                else:
                    a = browser.find_element_by_xpath('//*[@class="wxBaseinfo"]/p[2]').text
                    print(a)
                    gjc.append(a)
            else:
                print('关键词为空')
                gjc.append('关键词为空')
            if isPresentbyclass(browser, 'title'):
                a=browser.find_element_by_class_name('title').text
                titles.append(a)
                print(a)
            else:
                titles.append('null')
                print('null')
            if isPresentbyclass(browser, 'author'):
                a=browser.find_element_by_class_name('author').text
                author.append(a)
                print(a)
            else:
                author.append('null')
                print('null')
            if isPresentbyclass(browser, 'orgn'):
                a=browser.find_element_by_class_name('orgn').text
                orgn.append(a)
                print(a)
            else:
                orgn.append('null')
                print('null')
            if isPresentbypath(browser,'//*[@class="sourinfo"]/p'):
                a=browser.find_element_by_xpath('//*[@class="sourinfo"]/p').text
                paper.append(a)
                print(a)
            else:
                paper.append('null')
                print('null')
            # 期刊刊号
            if isPresentbypath(browser,'//*[@class="sourinfo"]/p[3]'):
                a=browser.find_element_by_xpath('//*[@class="sourinfo"]/p[3]').text
                paperdate.append(a)
                print(a)
            else:
                paperdate.append('null')
                print('null')
            if isPresentbypath(browser, '//*[@class="sourinfo"]/p[4]'):
                a = browser.find_element_by_xpath('//*[@class="sourinfo"]/p[4]').text
                issn.append(a)
                print(a)
            else:
                issn.append('null')
                print('null')
            print(tim)
            pubtime.append(tim)
            themes.append(theme)

            title = str(50 * (page - 1) + i + 1)
            url.append(browser.current_url)

            abstract = browser.find_element_by_xpath('//*[@id="ChDivSummary"]').text
            # 写入文件，每篇论文一个TXT文件，论文题目作为文件名
            write_to_file(title, abstract)
            print(abstract)
            abs.append(abstract)
            # 写入文档
            dataframe = pd.DataFrame(
                {'主题':themes,'文章标题': titles, '链接': url, '作者': author, '来源机构': orgn, '发表杂志': paper,
                 '发表时间':pubtime,'发表刊号':paperdate,'ISSN编号':issn,'关键词':gjc,'文章摘要': abs}
            )
            dataframe.to_csv("/Users/28028/Desktop/智业/爬虫示例/知网/知网爬虫.csv", index=False, encoding='utf_8_sig')
            print("第%d页第 %d 篇下载成功!!!" % (page, i + 1))
            print('--------------------------------------------------------'
                  '----------------------------------------------------------')

            # 关闭当前的窗口
        browser.close()
        # 下载结束要回到主窗口继续下一篇
        browser.switch_to_window(now_handle)


browser = webdriver.Chrome()
browser.get("http://kns.cnki.net/kns/brief/Default_Result.aspx?"
            "code=SCDB&kw=%e7%b3%bb%e7%bb%9f%e8%af%84%e4%bb%b7+%e5%8c%bb%e5%ad%a6&korder=0&sel=1")
browser.maximize_window()

time.sleep(3)
page = 1
page_num = 100

browser.switch_to.frame("iframeResult")
time.sleep(2)
browser.find_element_by_class_name('Ch').click()
time.sleep(2)
browser.find_element_by_xpath('//*[@class="Btn5"]/a').click()
time.sleep(2)
browser.find_element_by_xpath('//*[@id="id_grid_display_num"]/a[3]').click()
time.sleep(5)
# 跳页
# 9th
# browser.find_element_by_xpath('//*[@id="ctl00"]/table/tbody/tr[3]/td/table/tbody/tr/td/div/a[8]').click()
# time.sleep(5)
# # 最后一条
# browser.find_element_by_xpath('//*[@id="ctl00"]/table/tbody/tr[3]/td/table/tbody/tr/td/div/a[10]').click()
# time.sleep(2)
# browser.find_element_by_xpath('//*[@id="ctl00"]/table/tbody/tr[3]/td/table/tbody/tr/td/div/a[9]').click()
# time.sleep(5)

while page <= page_num:
    print('开始下载第 %d 页' % page)

    get_abstract(page, browser)

    switchNextPage(page, browser)

    page = page + 1
browser.quit()


# 诊疗指南、病例报告、临床研究、综述性文献以及系统评价类文献
# //*[@id="mainArea"]/div[3]/div[3]/div[1]/p[2]