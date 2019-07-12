# 自动爬取万方的每篇摘要连接并保存文件
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
# ！ 爬取知万方论文摘要：

# 自动翻页
def switchNextPage(browser):
    time.sleep(2)
    browser.find_element_by_class_name('laypage_next').click()
    all_handles = browser.window_handles#获取所有窗口句柄
    for handle in all_handles:#始终获得当前最后的窗口，所以要多次使用
            browser.switch_to_window(handle)

# 下载摘要
def get_abstract(browser):
    now_handle = browser.current_window_handle
    url=[]
    for i in range(1, 21):  # 每页二十篇论文
        # browser.switch_to_frame("iframeResult")
        time.sleep(3)
        si=str(i)
        browser.find_elements_by_xpath('//*[@id="aysnsearch"]/div/div['+si+']/div[2]/div[1]/a[1]')[0].click()

        # print(browser.find_elements_by_id('see_alldiv'))
        all_handles = browser.window_handles  # 获取所有窗口句柄
        for handle in all_handles:  # 始终获得当前最后的窗口，所以要多次使用
            browser.switch_to_window(handle)
        url=browser.current_url
        print(url)
        fobj = open('/Users/28028/Desktop/智业/爬虫示例/万方/医疗文章集链接.txt', 'a+')
        fobj.write(browser.current_url+'\n')
        fobj.close()
        print(i-1,'成功！------------------')
        # # 关闭当前的窗口
        browser.close()
        # # 下载结束要回到主窗口继续下一篇
        browser.switch_to_window(now_handle)


browser = webdriver.Chrome()
browser.get("http://www.wanfangdata.com.cn/search/searchList.do?searchType=all&showType=&pageSize=20&searchWord=%E8%AF%8A%E7%96%97%E6%8C%87%E5%8D%97&isTriggerTag=")
browser.maximize_window()


time.sleep(2)
browser.find_elements_by_xpath('//*[@id="laypage_0"]/a[6]')[0].click()
browser.find_element_by_class_name('laypage_next').click()
browser.find_element_by_class_name('laypage_next').click()


page = 1
page_num = 100
while page <= page_num:
    print('第 %d 页' % page)

    get_abstract(browser)

    switchNextPage(browser)

    page = page + 1
browser.quit()

