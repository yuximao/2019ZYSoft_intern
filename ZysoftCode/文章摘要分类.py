# 依次对每篇文章与四个字典做比对，看看哪个字典的匹配值最高，从而实现归类
import jieba
import jieba.posseg
from gensim import corpora,models,similarities
from collections import defaultdict
import pandas as pd

# 打开文件
jieba.load_userdict("mydicts.txt")
jieba.load_userdict("Neusoft_test/中文停用词库.txt")
# 制作字典语料库
alldoc=[]
paths=['字典/手术.txt','字典/检查.txt','字典/检验.txt','字典/疾病.txt','字典/药品.txt']
for path in paths:
    f = open(path,'r',encoding='utf-8')                         # 返回一个文件对象
    line = f.readline()                                         # 调用文件的 readline()方法
    doc=[]
    while line:
    # 后面跟 ',' 将忽略换行符
        a=line.strip('\n')
        txt_cut = jieba.posseg.cut(a)
        for i in txt_cut:
            if (i.flag == 'n'):
                a = str(i).replace("/n", "")
                doc.append(a)
        line = f.readline()
    alldoc.append(doc)

# 计算词频
frequency=defaultdict(int)
for text in alldoc:
    for word in text:
        frequency[word]+=1

# 生成新词典
dictionary=corpora.Dictionary(alldoc)
# dictionary.save("./dicto.txt")

# 制作要比对文档
df = pd.read_excel("科学网keytit.xlsx", usecols=[0],names=None)  # 读取项目名称列,不要列名
df_li = df.values.tolist()

res=[]
resname=[]
#要比对的文档分词
for s_li in df_li:
    try:
        testdoc = '' #存放当前摘要
        txt_encode = s_li[0]
        txt_cut = jieba.posseg.cut(txt_encode)
        for i in txt_cut:
            if (i.flag == 'n'):
                a=str(i).replace("/n","")
                testdoc+=a+' '
    except:
        testdoc='error'
    # 比对文档
    # 8、将要对比的文档通过doc2bow转化为稀疏向量
    new_xs=dictionary.doc2bow(testdoc.split())
    #9、对语料库进一步处理，得到新语料库
    corpus=[dictionary.doc2bow(text)for text in alldoc]
    #10、将新语料库通过tf-idf model 进行处理，得到tfidf
    tfidf=models.TfidfModel(corpus)
    #11、通过token2id得到特征数
    featurenum=len(dictionary.token2id.keys())
    #12、稀疏矩阵相似度，从而建立索引
    index=similarities.SparseMatrixSimilarity(tfidf[corpus],num_features=featurenum)
    #13、得到最终相似结果
    sim=index[tfidf[new_xs]]
    # print(testdoc)n
    lsim=sim.tolist()
    lname=lsim.index(max(lsim))
    if lname==0:
        resname.append('手术')
    elif lname==1:
        resname.append('检查')
    elif lname==2:
        resname.append('检验')
    elif lname==3:
        resname.append('疾病')
    else:
        resname.append('药品')
    res.append(sim)
    print(testdoc)

# 写结果
dataframe = pd.DataFrame(
    {'result': resname,'tfidf':res}
)
dataframe.to_csv("科学网摘要归类结果.csv", index=False, encoding='utf_8_sig')
