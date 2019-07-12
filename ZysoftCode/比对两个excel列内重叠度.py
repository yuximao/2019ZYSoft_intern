# 要比对每篇摘要的title是否在title库中存在
# 存在则写入
import pandas as pd
# 模糊化读文件
def readFile(name,line):
    df = pd.read_excel(name,encoding='utf-8', usecols=[line],names=None)  # 读取项目名称列,不要列名
    df_li = df.values.tolist()
    result_keyw = []
    for s_li in df_li:
        a=''
        for i in s_li[0]:
            if i.isalpha():
                a+=i
        result_keyw.append(a)
    return result_keyw
# 读全部内容
def readFile2(name,line):
    df = pd.read_excel(name,encoding='utf-8', usecols=[line],names=None)  # 读取项目名称列,不要列名
    df_li = df.values.tolist()
    result_keyw = []
    for s_li in df_li:
        result_keyw.append(s_li[0])
    return result_keyw
if __name__ == '__main__':
    # 创建指定长度的list
    lv='null'
    ll=6010
    llist=[lv for i in range(ll)]

    a=readFile('摘要内容.xlsx',0)
    a2=readFile2('摘要内容.xlsx',1)
    b=readFile('title汇总.xlsx',0)

    for i in range(len(a)):
        for j in range(len(b)):
            if b[j].find(a[i])!=-1 or a[i].find(b[j])!=-1:     #在1里面找'2'字符
                llist[j]=a2[i]
    # 写结果去文件
    dataframe = pd.DataFrame(
        {'result': llist}
    )
    dataframe.to_csv("重叠比对结果.csv", index=False, encoding='utf_8_sig')