import cx_Oracle
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
title=[]
db=cx_Oracle.connect('cmmi_ihr','cmmi_sehr','xmhealth')
print(db.version)
cur = db.cursor()
cur.execute('select NAME from DICT_ICD10_CODE ')
rows = cur.fetchall()
for row in rows[:20]:
   title.append(str(f"{row[0]} ,").strip(','))
print(title)



# 开始比对
import pandas as pd
from openpyxl import load_workbook
import openpyxl

# 读字典
f = open("mydic.txt",'r',encoding='utf-8')             # 返回一个文件对象
line = f.readline()             # 调用文件的 readline()方法
medworld=[]
while line:
# 后面跟 ',' 将忽略换行符
    a=line.strip('\n')
    if len(a)>0:
        medworld.append(a)
    line = f.readline()
f.close()

freq=[]
wrds=[]
# 比对
for i in title:
    wrd=''
    ii=0 #匹配中词语个数
    for j in medworld:
        if i.find(j)!=-1:
            ii+=1
            wrd+=j+'  '
            # print(j) #匹配的词语
    # print(i,ii)
    freq.append(ii)
    wrds.append(wrd)
    # print('-----------------------------------------------------------------')

# 写csv
dataframe = pd.DataFrame(
    {'title': title,'freq':freq,'words':wrds}
)
dataframe.to_csv("Oracle_result.csv", index=False, encoding='utf_8_sig')

