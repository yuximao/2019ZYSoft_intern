#-*- coding:utf-8 -*-
"""
    使用tf-idf对爱爱医学的文章进行分类，分别分为手术、检查、检验、疾病和药品五个大类。
"""
import pandas as pd
import jieba
import jieba.posseg
import numpy as np
from gensim import corpora,models,similarities
from collections import defaultdict
jieba.load_userdict("mydicts.txt")  # 导入词典
jieba.load_userdict("中文停用词库.txt")  # 下载停用词
path = r"字典/药品.csv"  # 词典路径
shoushu = pd.read_csv(path, header=0, usecols=[0])
fa = open(r"字典/药品.txt", "a+", encoding="utf-8")
article = pd.read_csv("爱爱医学文章文章内容切词.csv", usecols=[0])  # 待分配文件
result = open(r"字典/结果.txt", "a+", encoding="utf-8")

def cut_dict():
    """
    对词典进行切割，挑选出名词。
    """
    for sen in shoushu.values:
        sen = str(sen)
        sen = sen.replace("'", "")
        sen = sen.replace("\n", "")
        sen = sen.replace("[", "")
        sen = sen.replace("]", "")
        sen = jieba.posseg.cut(str(sen))
        for i in sen:
            if i.flag == "n":
                fa.write(i.word)
                fa.write("\n")
    fa.close()

# 所有文档
def make_dict():
    """
    制作医学词典
    :return: 返回所有的词典集合
    """
    alldoc=[]
    paths=['字典/手术.txt','字典/检查.txt','字典/检验.txt','字典/疾病.txt','字典/药品.txt']
    for path in paths:
        f = open(path,'r',encoding='utf-8')             # 返回一个文件对象
        line = f.readline()                                         # 调用文件的 readline()方法
        doc=[]
        while line:
        # 后面跟 ',' 将忽略换行符
            a=line.strip('\n')
            doc.append(a)
            line = f.readline()
        alldoc.append(doc)
    return alldoc

def calculate_word_frequency(alldoc):
    """
    计算词频
    :param alldoc: 需要被分类的分档
    :return: 排序之后的文件
    """
    frequency = defaultdict(int)
    for text in alldoc:
        for word in text:
            frequency[word] += 1
    # 生成新词典
    dictionary = corpora.Dictionary(alldoc)
    dictionary.save("字典/newdicts.txt")
    res = []
    for sen in article.values:
        sen = str(sen)
        sen = sen.replace("'", "")
        sen = sen.replace("\n", "")
        sen = sen.replace("[", "")
        sen = sen.replace("]", "")
        sen = sen.replace(",", "")
        new_xs=dictionary.doc2bow(sen.split())
        # 9、对语料库进一步处理，得到新语料库
        corpus=[dictionary.doc2bow(text)for text in alldoc]
        # 10、将新语料库通过tf-idf model 进行处理，得到tfidf
        tfidf=models.TfidfModel(corpus)
        # 11、通过token2id得到特征数
        featurenum=len(dictionary.token2id.keys())
        # 12、稀疏矩阵相似度，从而建立索引
        index=similarities.SparseMatrixSimilarity(tfidf[corpus],num_features=featurenum)
        # 13、得到最终相似结果
        sim=index[tfidf[new_xs]]
        suoyin = np.argmax(sim)
        result.write(str(suoyin))
        result.write("\n")
        res.append(suoyin)
    dataframe = pd.DataFrame(
        {'排序': res}
    )
    dataframe.to_csv("字典/排序.csv", index=False, header=None, encoding='utf_8_sig')


if __name__=="__main__":
    alldoc = make_dict()
    calculate_word_frequency(alldoc)
    result.close()