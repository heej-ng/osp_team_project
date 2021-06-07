#!/usr/bin/python3
#-*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup

url = u'https://finance.naver.com/sise/lastsearch2.nhn'
res = requests.get(url)
html = BeautifulSoup(res.content, "html.parser")
html_table = html.find(class_="type_5")
html_list = html_table.find_all("a", limit=15)	#인기 순위 15개 html_list에 저장
for x in html_list:
        y = x.text
        print(y)	#종목명 출력

