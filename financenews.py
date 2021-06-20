#!/usr/bin/python3
#-*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
import datetime

if __name__ == '__main__':
	now = datetime.datetime.now()
	newslink = []
	newstitle = []
	for i in range(1):#오늘 많이 본 기사 끌어오기
		newscontent = []
		datestr = now.strftime('%Y%m%d')
		url = 'https://finance.naver.com/news/news_list.nhn?mode=RANK&date=' + datestr
		res = requests.get(url)
		html = BeautifulSoup(res.content, 'html.parser')
		newslist = html.find_all(attrs={'class':'simpleNewsList'})
		for j in newslist:
			newslist2 = j.find_all('a')
			for k in newslist2:
				newslink.append(k['href'])
				newstitle.append(k['title'])
		#print(newslink)
		print(newstitle)
		for j in newslink:
			newsurl = 'https://finance.naver.com' + j
			newsres = requests.get(newsurl)
			newshtml = BeautifulSoup(newsres.content, 'html.parser')
			content = newshtml.find(attrs={'class':'articleCont'})
			for text in content.find_all(text=True):
				if(text.parent.name == "div"):
					print(text)
		now = now - datetime.timedelta(1)

