import jieba
import jieba.posseg
import jieba.analyse.textrank
import pandas as pd
from collections import Counter


line=[]
jieba.load_userdict("mydicts.txt")
jieba.load_userdict("Neusoft_test/中文停用词库.txt")
df = pd.read_excel("知网.xlsx", usecols=[0],names=None)  # 读取项目名称列,不要列名
df_li = df.values.tolist()
# result_tit = []
for s_li in df_li[:100]:
    l = ''
    # result_tit.append(s_li[0])
    txt_encode = s_li[0].encode('utf-8')
    txt_cut = jieba.posseg.cut(txt_encode)
    for i in txt_cut:
        if (i.flag == 'n'):
            l+=str(i)
    a=jieba.analyse.textrank(l, topK=20, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v'))
    line.append(a)
print(line)

#二次比对
f = open("newdict.txt",'r',encoding='utf-8')             # 返回一个文件对象
line = f.readline()                                         # 调用文件的 readline()方法
medworld=[]
while line:
# 后面跟 ',' 将忽略换行符
    a=line.strip('\n')
    if len(a)>1:
        medworld.append(a)
    line = f.readline()

for i in l:
    isok=0
    for j in medworld:
        if (j==i) or (i=='\n'):
            isok=1
            break
    if isok==0:
        l.remove(i)

# 排序
result = Counter(l)
# 排序
d = sorted(result.items(), key=lambda x: x[1], reverse=True)
print(d)
# print(l)

with open('res_nodic.txt', 'w') as f2:    # 分词结果写入文件保存
    for i in d:
        f2.write(str(i)+' ')
f2.close()
