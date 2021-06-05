
from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import datetime

code = input()

# 네이버 증권에서 크롤링
일자 = []
종가 = []
거래량 = []
info_dataframe = []

for i in range(10):
    url = 'https://finance.naver.com/item/sise_day.nhn?code={}&page={}'.format(code, str(i+1))
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find(class_='type2')
    print(table)
    date = table.find_all("span", {"class": "tah p10 gray03"})
    info = table.find_all("span", {"class": "tah p11"})


    # info 리스트로 들어온 값 중 0을 제외시켜주어야 정상적으로 데이터를 추출
    del_index = []
    for r in range(len(info)):
        if(info[r].text == '0'):
            del_index.append(r)
    for index in del_index:
        del info[index]


    for j in range(0, len(date)): # 일자, 종가, 거래량 크롤링
        일자.append(date[j].text)
        종가.append(int((info[j*5].text).replace(',', '')))
        거래량.append(int((info[j*5+4].text).replace(',', '')))


info_list = {'일자': 일자, '종가': 종가, '거래량': 거래량}

# padas로
일자 = pd.to_datetime(일자)
for elements in info_list.values():
    elements = pd.DataFrame(elements)
    info_dataframe.append(elements)

result = pd.concat(info_dataframe[1:], axis=1)
result.index = 일자
result.colums = ['종가', '거래량']

# 그래프 그리기
fig = plt.figure(figsize=(12, 8))
top_axes = plt.subplot2grid((4, 4), (0, 0), rowspan=3, colspan=4)
bottom_axes = plt.subplot2grid((4, 4), (3, 0), rowspan=1, colspan=4)
top_axes.plot(일자, 종가)
bottom_axes.bar(일자, 거래량)
plt.show()
