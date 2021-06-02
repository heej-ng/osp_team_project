#!/usr/bin/python3

from bs4 import BeautifulSoup
import requests

url = "https://finance.naver.com/sise/sise_market_sum.nhn?page=1"
result = requests.get(url)
soup = BeautifulSoup(result.text, 'lxml')

stock_head = soup.find("thead").find_all("th")
data_head = [head.get_text() for head in stock_head]

stock_list = soup.find("table", attrs={"class":"type_2"}).find("tbody").find_all("tr")

# 출력 정보 ['N', '종목명', '현재가', '전일비', '등락률', '액면가', '시가총액', '상장주식수', '외국인비율', '거래량', 'PER', 'ROE', '토론실']

for stock in stock_list:
	if len(stock) > 1:
		print(stock.get_text().split())
