#!/usr/bin/python3

from bs4 import BeautifulSoup
from datetime import datetime
import requests
import time

def get_code(company_code):
	url = "https://finance.naver.com/item/main.nhn?code=" + company_code
	result = requests.get(url)
	bs_obj = BeautifulSoup(result.content, "html.parser")
	return bs_obj

def get_price(company_code):
	bs_obj = get_code(company_code)
	no_today = bs_obj.find("p", {"class":"no_today"})
	blind = no_today.find("span", {"class":"blind"})
	now_price = blind.text
	return now_price

company_codes = ["005930","003490","028050"]

while True:
	now = datetime.now()
	print(now)

	for item in company_codes:
		now_price = get_price(item)
		print(now_price)
	print("----------------------------------")
	time.sleep(10)

