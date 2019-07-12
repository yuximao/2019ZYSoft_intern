# -*— coding:utf-8 -*-
"""
 @author   : sc
 @Function : 爬虫——爬取爱爱医医疗网站文章，全部合并
"""
import os
import pandas as pd
path = r'G:\汇总2\汇总添加作者csv\医疗病例\爱爱医学'
pathlist = os.listdir(path)
for i in pathlist:
    paths = path+"\\"+i  # 'G:\医疗文章\爱爱医学\中医科'
    pathlists = os.listdir(paths)
    k = 0
    for u in pathlists:
        pathcontent = paths +"\\"+u # 'G:\医疗文章\爱爱医学\中医科\中医五官科'
        source = pathcontent + "\\"+u+".csv"
        print(source)
        fb = pd.read_csv(source)
        fb.to_csv(path+"\\"+"爱爱医病例合并.csv",mode='a', index=False, header=False,encoding="utf_8_sig")
