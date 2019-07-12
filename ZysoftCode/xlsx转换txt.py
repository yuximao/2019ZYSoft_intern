
import pandas as pd
listname=[]
df = pd.read_excel("知网.xlsx", usecols=[0],names=None)  # 读取项目名称列,不要列名
df_li = df.values.tolist()
for s_li in df_li:
    testdoc = '' #存放当前摘要
    txt_encode = s_li[0].encode('GBK')
    listname.append(txt_encode)

file_write_obj = open("知网摘要.txt", 'w')

for var in listname:
    file_write_obj.writelines(str(var))
    file_write_obj.write('\n')
file_write_obj.close()
