import pandas as pd
dataform=[]
df = pd.read_excel("知网标题关键词.xlsx", usecols=[0],names=None)  # 读取项目名称列,不要列名
df2 = pd.read_excel("知网标题关键词.xlsx", usecols=[1],names=None)
df_li = df.values.tolist()
df_li2 = df2.values.tolist()
for i in range(len(df_li)):
    testdoc = '' #存放当前摘要
    txt_encode = df_li[i][0]
    txt_encode2=df_li2[i][0]
    # print(txt_encode,txt_encode2)
    dataform.append(txt_encode+txt_encode2)
# print(dataform)

# 写入文件
dataframe = pd.DataFrame(
    {'result': dataform}
)
dataframe.to_csv("知网合并.csv", index=False, encoding='utf_8_sig')
