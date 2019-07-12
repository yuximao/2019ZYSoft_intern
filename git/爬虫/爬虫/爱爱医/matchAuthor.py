# -*— coding:utf-8 -*-
"""
 @author   : sc
 @Function : 爬虫——爬取爱爱医医疗网站文章获取医生匿名和真实姓名
"""
import pandas as pd
import os
path = r"G:\汇总添加作者csv\医疗文章\爱爱医学\爱爱医学"
pathlist = os.listdir(path)
dicts = {}
dnames = []
snames = []
for i in pathlist:
    paths = path+"\\"+i  # 'G:\医疗文章\爱爱医学\中医科'
    pathlists = os.listdir(paths)
    for j in pathlists:
        pathcontent = paths + "\\" + j  # 'G:\医疗文章\爱爱医学\中医科\中医五官科'
        source = pathcontent + "\\" + j + "作者.csv"
        fa = pd.read_csv(source)
        doctorname = fa.pop("医生姓名")
        screenname = fa.pop("医生匿名")
        for k in range(len(doctorname)):
            dnames.append(doctorname[k])
        for u in range(len(screenname)):
            snames.append(screenname[u])
dn = list(zip(dnames,snames))
print(len(dn))
# fb = open("G:\汇总添加作者csv\医疗文章\爱爱医学\\"+"医生姓名匿名.txt","a+", encoding="utf-8")
# fb.write(str(dn))