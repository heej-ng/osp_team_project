#!/usr/bin/python3
#-*- coding: utf-8 -*-

import math
import re
import requests
from bs4 import BeautifulSoup, NavigableString
from konlpy.tag import *
import datetime

total_word = {}

def hfilter(s):
	return re.sub(u'[^ \.\,\?\!\u0041-\u005A\u0061-\u007A\uac00-\ud7a3]+','',s)
#	return re.sub(u'[^ \.\,\?\!\uac00-\ud7a3]+','',s)

def compute_tf(s):
	tf_d = {}
	for word,count in s.items():
		tf_d[word] = count / float(len(s))

	return tf_d

def compute_idf(sent_list):
	idf_d = {}
	for t in total_word:
		cnt = 0
		for s in sent_list:
			if t in s:
				cnt += 1
		idf_d[t] = math.log(len(sent_list)/float(cnt))

	return idf_d

def news_issue():
	now = datetime.datetime.now()
	texttemp = []
	textlist = []
	sent_list = []
	wlist = {}
	tf_list = []
	tfcount = 0
#	mecab = Mecab()
	okt = Okt()

	for i in range(2): #오늘 많이 본 기사 끌어오기
		newslink = []
		datestr = now.strftime('%Y%m%d')
		url = 'https://finance.naver.com/news/news_list.nhn?mode=RANK&date=' + datestr
		res = requests.get(url)
		html = BeautifulSoup(res.content, 'html.parser')
		newslist = html.find_all(attrs={'class':'simpleNewsList'})
		for j in newslist:
			newslist2 = j.find_all('a')
			for k in newslist2:
				newslink.append(k['href'])
		for j in newslink: #뉴스 기사별 반복
			article = []
			newsurl = 'https://finance.naver.com' + j
			newsres = requests.get(newsurl)
			newshtml = BeautifulSoup(newsres.content, 'html.parser')
			content = newshtml.find(attrs={'class':'articleCont'})
			text = content.find_all(text=True)
			for t in text: #본문 문단별 반복
				if t.parent.name == "div":
					if t != ' ' and t != '\n':
						num = -1
						while t[num] == ' ':
							num -= 1
						if t[num] == '.':
							t = re.sub(r'\([^)]*\)', '', t)
							t = re.sub(r'\[[^)]*\]', '', t)
							article.append(t)
			article2 = ''.join(article)
			textlist.append(hfilter(article2).split('.'))

		for j in textlist:	#한 기사
			word_d = {}
			idf_list = []
			for k in j:	#한 줄
#				wlist = mecab.nouns(k)
				wlist = okt.nouns(k)

				for w in wlist:
#					mw = mecab.pos(w)
#					if w not in word_d and mw[0][1] == "NNP":
					if w not in word_d:
						word_d[w] = 1
						idf_list.append(w)
						total_word[w] = 1
#					elif mw[0][1] == "NNP":
					else:
						word_d[w] += 1
						total_word[w] += 1

			tf_d = compute_tf(word_d)
			tf_list.append(tf_d)
			sent_list.append(idf_list)
			tfcount += 1

		now = now - datetime.timedelta(1)

	idf_d = compute_idf(sent_list)

	tf_idf_list = []
	for tf in tf_list:
		tf_idf = {}	
		for word, tfval in tf.items():
			tf_idf[word] = tfval * idf_d[word]
		tf_idf_list.append(tf_idf)
	
	issue = {}

	for word, key in idf_d.items(): # 추출된 단어들 하나씩 선택
		max = 0
		for doc in tf_idf_list: # tf_idf 계산한 list에서 한 행(뉴스)에 사용된 단어의 max tf-idf값 선택
			if word not in doc.keys():
				continue
			elif doc[word] > max:
				max = doc[word]
				issue[word] = max
			else:
				continue

	hot_issue = {}
	for w,c in sorted(issue.items(), key=lambda x:x[1], reverse=True):
		if len(w) >= 3:
			hot_issue[w] = c

	top15 = {}
	
	icnt = 0
	for w,c in hot_issue.items():
		if icnt == 15:
			break
		else:
			icnt += 1
			top15[w] = 20 - icnt
	return top15
