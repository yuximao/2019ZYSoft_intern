import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json
import time

def es_scan(client, index, doc, query_dict=None):
    """
    :param client: es服务（Elasticsearch）
    :param index: 索引（str）
    :param doc: 类型（str)
    :param query_dict: 查询body（dict）
    :return: 查询结果json  # 查询结果（DataFrame）
    """
    result_list = []
    if query_dict is None:
        search_data = helpers.scan(client=client, scroll='5m', index=index, doc_type=doc,
                                   timeout="1m")
    else:
        query_dict_n = {"query": query_dict}
        search_data = helpers.scan(client=client, query=query_dict_n, scroll='5m', index=index, doc_type=doc,
                                   timeout="1m")
    # for item in search_data:
    #     data_source = item['_source']
    #     result_list.append(data_source)
    # result_df = pd.DataFrame(result_list)
    return search_data


# 比较运算符字符串计算解析
def operator_analysis(val1, val2, str_operator):
    """
    :param val1: 比较运算左侧变量
    :param val2: 比较运算右侧变量
    :param str_operator: 比较运算符
    :return: 返回对比结果的布尔值
    """
    if str_operator == '>=':
        a = (val1 >= val2)
    elif str_operator == '>':
        a = (val1 > val2)
    elif str_operator == '<=':
        a = (val1 <= val2)
    elif str_operator == '<':
        a = (val1 < val2)
    else:  # str_operator == '==':
        a = (val1 == val2)
    return a
class IcdGradeRule:
    def __init__(self, client):
        self.client = client
    # 字典
    def get_icd_dict(self, index='ihr-dictionary', doc='dict_icd10_code'):
        """
        :param client: ES连接
        :param index: 索引
        :param doc: 类型
        :return: icd字典的DataFrame(['disease_id', 'icd_code', 'subcode', 'name'])
        """
        query_dict = {"bool": {"must": [
            {"match": {
            "version.keyword": "GBT15657-1995"
             }
            },
            # {"match": {
            # "version.keyword": "China2016"
            #  }
            # },
            # {"term": {
            #     "is_last": {
            #         "value": 1
            #     }
            # }}
        ]}}
        client = self.client
        icd_data_json = es_scan(client, index, doc, query_dict)
        icd_data_tmp = pd.DataFrame(icd_data_json)
        icd_data_all_id = icd_data_tmp['_id']
        icd_data_all_source = icd_data_tmp['_source']
        icd_data_all_source = pd.DataFrame(icd_data_all_source.tolist())
        icd_data_all = pd.concat([icd_data_all_id, icd_data_all_source], axis=1)
        icd_data_all = icd_data_all.loc[:, ['_id', 'code', 'subcode', 'name']]
        icd_data_all.rename(columns={'_id': 'disease_id', 'code': 'icd_code'}, inplace=True)
        # icd_main = icd_data_all.loc[icd_data_all['icd_code'].notnull()]
        # icd_sub = icd_data_all.loc[icd_data_all['icd_code'].isnull(), ['disease_id', 'subcode', 'name']]
        # icd_sub.rename(columns={'subcode': 'icd_code'}, inplace=True)
        # icd_etl = pd.merge(icd_sub, icd_main, on=['icd_code'], how='left')
        # icd_sub_etl = icd_etl.loc[icd_etl['name_y'].isnull()]  # 与主码重复的部分去掉
        # icd_sub_etl.loc[:, 'subcode'] = icd_sub_etl['icd_code']
        # icd_sub_etl.loc[:, 'name'] = icd_sub_etl['name_x']
        # icd_sub_etl.loc[:, 'disease_id'] = icd_sub_etl['disease_id_x']
        # icd_sub_etl.drop(['name_x', 'name_y', 'disease_id_x', 'disease_id_y', 'icd_code', 'subcode'], axis=1,
        #                  inplace=True)
        # icd_data = pd.concat([icd_main, icd_sub_etl], axis=0, sort=True)  # 合并后
        # icd_data.drop(['icd_code', 'subcode'], axis=1, inplace=True)
        # icd_data.rename(columns={'name': 'class_name'}, inplace=True)
        return icd_data_all

        # 获取疾病分类数据,并做初步处理

    def get_diagnosis_classify(self):
        """
        :param client: ES连接
        :return: 分类疾病的DataFrame(['disease_id','name'])
        """
        client = self.client
        diagnosis_classify_tmp = es_scan(client, 'ihr-diagnosis', 'icd_diagnosis_classify')
        diagnosis_classify_tmp = pd.DataFrame(diagnosis_classify_tmp)
        diagnosis_classify_tmp_id = diagnosis_classify_tmp['_id']
        diagnosis_classify_tmp_source = diagnosis_classify_tmp['_source']
        # diagnosis_classify_all = diagnosis_classify_all.loc[:, ['_id', '_source']]
        diagnosis_classify_tmp_source = pd.DataFrame(diagnosis_classify_tmp_source.tolist())
        diagnosis_classify_all = pd.concat([diagnosis_classify_tmp_id, diagnosis_classify_tmp_source], axis=1)
        # diagnosis_classify_all = diagnosis_classify_all.groupby('_id', as_index=False).apply(
        #     lambda x: pd.DataFrame([x['_source'].values[0]]))  # 此种方式效率低

        diagnosis_classify = diagnosis_classify_all.loc[:, ['icd_list']]
        print(diagnosis_classify)
        llist=list(diagnosis_classify)
        print(llist)
        # diagnosis_classify.rename(columns={'icd_list': 'disease_id'}, inplace=True)
        return diagnosis_classify
    def get_grade_rule(self):

        """
        :return: DataFrame——获取分级规则的疾病并与分类数据、icd关联上
        """

        # 用于将规则中病史的疾病列表中每个disease_id对照name，以d形成的list返回结果
        def disease_id_name(disease_list, map_dict):
            disease_map_list = []
            for disease in disease_list:
                disease_dict = {'disease_id': disease}
                disease_map_df = map_dict.loc[map_dict['disease_id'] == disease]
                disease_name = disease_map_df['class_name'].values[0]
                disease_dict['class_name'] = disease_name
                disease_map_list.append(disease_name)
            return disease_map_list

        #
        grade_rule_data = es_scan(self.client, index='ihr-dictionary', doc='dict_icd10_code')  # , query_dict
        grade_rule_data = pd.DataFrame(grade_rule_data)
        grade_rule_data = grade_rule_data['_source']
        grade_rule_data = pd.DataFrame(grade_rule_data.tolist())
        # grade_rule_root = grade_rule_data.loc[grade_rule_data['category'] == 0]
        icd_data = self.get_icd_dict()
        classify_data = self.get_diagnosis_classify()
        # ICD10字典与classify_data可能具有包含关系（classify_data里的ICD可能为大类），认为不处理不影响结果，因此暂不处理。
        disease_data = pd.concat([icd_data, classify_data], axis=0, sort=True)
        # step1:关联疾病根节点
        grade_disease = pd.merge(disease_data, grade_rule_data, on='disease_id', how='inner')
        # step2:关联病史
        grade_disease['history_etl'] = ''
        grade_disease.loc[grade_disease['cond_type'] == 4, 'history_etl'] = grade_disease.loc[
            grade_disease['cond_type'] == 4, 'values'].apply(lambda x: disease_id_name(x, disease_data))
        return grade_disease


if __name__ == '__main__':
    time1 = time.time()
    hosts = ['192.168.3.49:9200', '192.168.3.50:9200', '192.168.3.51:9200', '192.168.3.52:9200', '192.168.3.53:9200']
    client_local = Elasticsearch(hosts=hosts)
    # icd_classify_data = icd_classify(client)
    grade_rule = IcdGradeRule(client_local).get_grade_rule()
    time2 = time.time()
    print('疾病细层与规则关联：' + str(round(time2 - time1, 5)))
