# silienum示例
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time

browser = webdriver.Chrome()
browser.get("http://kns.cnki.net/kns/brief/result.aspx?dbprefix=SCDB&crossDbcodes=CJFQ,CDFD,CMFD,CPFD,IPFD,CCND,CCJD")
browser.maximize_window()
#
# # # 定位父类层级iframe
# # ele_framest = driver.find_element_by_css_selector('#result > iframe')

# 切换到父类层级iframe-通过元素切换
# browser.switch_to.frame("iframeResult")
# print(browser.page_source)
# print("-----------------------------------------------")


# 下载iframe---------------------------------------------------------------------------------------------------------------------------------------------
for i in range(0, 20):  # 每页二十篇论文
    browser.switch_to.frame("iframeResult")
    # time.sleep(5)
    browser.find_elements_by_class_name('fz14')[i].click()
    # browser.find_elements_by_xpath('//*[@id="ctl00"]/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/a').click()
    all_handles = browser.window_handles  # 获取所有窗口句柄
    for handle in all_handles:  # 始终获得当前最后的窗口，所以要多次使用
        browser.switch_to_window(handle)
    # 获取论文题目
    # title=browser.find_element_by_class_name('title').text
    # title=browser.find_element_by_xpath("//*[@id='mainArea']/div[3]/div[1]/h2").text
    title = str(20 * (page - 1) + i + 1)
    if isPresent(browser, 'ChDivSummary'):
        abstract = browser.find_element_by_xpath('//*[@id="ChDivSummary"]').text
        # 写入文件，每篇论文一个TXT文件，论文题目作为文件名
        # write_to_file(title, abstract)
        print(abstract)
        print("第%d页第 %d 篇下载成功!!!" % (page, i + 1))

# #
# # # 切换到第二个子类frame-通过索引切换
# # driver.switch_to.frame(1)
# # print(driver.page_source)
# # print("-----------------------------------------------")
# #
# # # 切换到最上层层级-等同于driver.switch_to_frame(None)
# # driver.switch_to_default_content()


