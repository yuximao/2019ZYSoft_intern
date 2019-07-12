# -*-coding:utf-8 -*-
"""
 @author   : sc
 @Function : 爬虫——爬取爱爱医医疗网站文章，进行合并
"""
import os
import pandas as pd
path = r'G:\汇总2\汇总添加作者csv\医疗文章\爱爱医学\爱爱医学'
pathlist = os.listdir(path)
for i in pathlist:
    paths = path+"\\"+i  # 'G:\医疗文章\爱爱医学\中医科'
    pathlists = os.listdir(paths)
    k = 0
    for u in pathlists:
        pathcontent = paths +"\\"+u # 'G:\医疗文章\爱爱医学\中医科\中医五官科'
        source = pathcontent + "\\"+u+".csv"
        src = pathcontent + "\\"+u+"作者.csv"
        fa = pd.read_csv(src)
        fb = pd.read_csv(source)
        doctorname = fa.pop("医生姓名")
        belongke = fa.pop("隶属科室")
        doctortitle = fa.pop("医生职称")
        screenname = fa.pop("医生匿名")
        skills = fa.pop("擅长")
        briefs = fa.pop("简介")
        fb["医生姓名"] = doctorname
        fb["隶属科室"]=belongke
        fb["医生职称"]=doctortitle
        fb["医生匿名"]=screenname
        fb["擅长"]=skills
        fb["简介"]=briefs
        fb.to_csv(pathcontent+"\\"+u+"合并.csv",columns=['文章标题','日期','浏览次数','文章内容','导读','科室一级','科室二级','医生姓名',
                                                       "隶属科室","医生职称","医生匿名","擅长","简介"],index=0,header=1,encoding="utf_8_sig")
        print("end")