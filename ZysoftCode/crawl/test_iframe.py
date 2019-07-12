# 破解iframe
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pandas as pd
from time import sleep
import time


browser = webdriver.Chrome()
browser.get("http://kns.cnki.net/kns/brief/Default_Result.aspx?code=SCDB&kw=%E6%84%9F%E5%86%92&korder=0&sel=1")
browser.maximize_window()

time.sleep(8)


browser.switch_to.frame("iframeResult")
urls = browser.find_elements_by_class_name("fz14")
for url in urls:
    print(url.get_attribute("href"))
