#!/usr/bin/python3
#-*- coding: utf-8 -*-
import sys
import re
import requests
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch

es_host="127.0.0.1"
es_port="9200"
es = Elasticsearch([{'host':es_host,'port':es_port}], timeout=30)

company_name=['삼성전자','SK하이닉스','카카오','NAVER','삼성전자우','LG화학','삼성바이오로직스','현대차','삼성SDI','셀트리온','기아','POSCO','현대모비스','LG생활건강','LG전자','SK이노베이션','삼성물산','SK텔레콤','KB금융','신한지주']
company_code=['005930','000660','035720','035420','005935','051910','207940','005380','006400','068270','000270','005490','012330','051900','066570','096770','028260','017670','105560','055550']

name_to_code={'삼성전자' : '005930', 'SK하이닉스' : '000660', '카카오' : '035720', 'NAVER' : '035420', '삼성전자우' : '005935', 'LG화학' : '051910', '삼성바이오로직스' : '207940', '현대차' : '005380', '삼성SDI' : '006400', '셀트리온' : '068270', '기아' : '000270', 'POSCO' : '005490', '현대모비스' : '012330', 'LG생활건강' : '051900', 'LG전자' : '066570', 'SK이노베이션' : '096770', '삼성물산' : '028260', 'SK텔레콤' : '017670', 'KB금융' : '105560', '신한지주' : '055550'}
code_to_name={'005930' : '삼성전자', '000660' : 'SK하이닉스', '035720' : '카카오', '035420' : 'NAVER', '005935' : '삼성전자우', '051910' : 'LG화학', '207940' : '삼성바이오로직스', '005380' : '현대차', '006400' : '삼성SDI', '068270' : '셀트리온', '000270' : '기아', '005490' : 'POSCO', '012330' : '현대모비스', '051900' : 'LG생활건강', '066570' : 'LG전자', '096770' : 'SK이노베이션', '028260' : '삼성물산', '017670' : 'SK텔레콤', '105560' : 'KB금융', '055550' : '신한지주'}

def get_elastic_data(id):
    index = 'day'
    type = 'price'
    body = {
        'query': {'match_all': {}}
    }
    res = es.get(index=index, doc_type=type, id=id)
    #print(res)
    print(res['_source']['price'])
    list=res['_source']['price']
    return list

def stable_recommend_algo(res):
    aver_list = []
    pattern = '[^\w\s]'
    repl = ''
    print(len(res))
    print(len(res) / 5)
    for i in range(0, len(res) - 4, 5):
        sum = 0
        for j in range(i, i + 5, 1):
            a = 0
            a = re.sub(pattern=pattern, repl=repl, string=res[j])
            sum += int(a)
        aver = sum / 5
        aver_list.append(aver)

    print(len(aver_list))
    print(aver_list)
    down_cnt = 0
    cnt = 0
    for i in range(0, len(aver_list) - 1):
        diff = aver_list[i] - aver_list[i + 1]
        if (diff < (aver_list[i] * 0.05 * (-1))):
            down_cnt += 1
        cnt += 1
    print(cnt)
    if (down_cnt > 5):
        print('rightdown')
        return 0
    else:
        print('rightup')
        return 1

def danger_recommend_algo(res):
    aver_list = []
    pattern = '[^\w\s]'
    repl = ''
    print(len(res))
    print(len(res) / 5)
    for i in range(0, len(res) - 4, 5):
        sum = 0
        for j in range(i, i + 5, 1):
            a = 0
            a = re.sub(pattern=pattern, repl=repl, string=res[j])
            sum += int(a)
        aver = sum / 5
        aver_list.append(aver)

    print(len(aver_list))
    print(aver_list)
    up_cnt = 0
    cnt = 0
    for i in range(0, len(aver_list) - 1):
        diff = aver_list[i] - aver_list[i + 1]
        if (diff > (aver_list[i] * 0.04)):
            up_cnt += 1
        cnt += 1
    print(cnt)
    if (up_cnt > 20):
        print('rightup')
        return 1
    else:
        print('rightdown')
        return 0

def recom_algo(type):
    stable_list=[]
    danger_list=[]
    reco_list=[]
    for i in range(0,20):
        list = get_elastic_data(company_name[i])
        if(stable_recommend_algo(list)):
            stable_list.append(company_name[i])
        if(danger_recommend_algo(list)):
            danger_list.append(company_name[i])
    #print('stable : ')
    #print(stable_list)
    #print('danger : ')
    #print(danger_list)

    if(type=='stable'):
        return stable_list
    elif(type=='danger'):
        return danger_list


