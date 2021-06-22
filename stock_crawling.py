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

def day_stock_crawling(code):
    # 2. 웹 크롤링
    # 2021년 1월 7일, 네이버가 웹크롤링 차단 실시
    # 네이버 금융서버에서 http 패킷 헤더의 웹 브라우저 정보(User-agent)를 체크
    # 웹 브라우저 정보를 함께 전송해야 한다.
    url = 'https://finance.naver.com/item/sise_day.nhn?code=005930&page=1'
    with requests.get(url, headers={'User-agent': 'Mozilla/5.0'}) as doc: # <== 이처럼 브라우저 정보를 requests 모듈을 이용해 전송해야 한다.
        html = BeautifulSoup(doc.text, "lxml")
        pgrr = html.find('td', class_='pgRR')
        s = str(pgrr.a['href']).split('=')
        last_page = s[-1]
        #print(last_page)

    date=[]
    price=[]
    sise_url = 'https://finance.naver.com/item/sise_day.nhn?code=' + code
    # for page in range(1, int(last_page)+1):
    for page in range(1, 50):
        page_url = '{}&page={}'.format(sise_url, page)
        response_page = requests.get(page_url, headers={'User-agent': 'Mozilla/5.0'}).text
        html = BeautifulSoup(response_page, 'html.parser')
        main = html.find('table', {'class': 'type2'})
        main0 = main.find_all('tr', {'onmouseover': 'mouseOver(this)'})
        for i in range(len(main0)):
            d=main0[i].find('td', {'align':'center'})
            p=main0[i].find('td', {'class':'num'})
            date.append(d.get_text())
            price.append(p.get_text())

    print(date)
    print('---------------')
    print(price)
    print("zzzz")
    print(len(date))
    print(len(price)) #490

    name=code_to_name[code]
    print(name)
    ela_dict = {"date": date, "price": price}
    res = es.index(index='day', doc_type='price', id=name, body=ela_dict)
    print(res)


def stock_crawling():
    #for i in range(len(company_code)):
    for i in range(0,20):
        day_stock_crawling(company_code[i])


