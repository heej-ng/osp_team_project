#!/usr/bin/python3
#-*- coding: utf-8 -*-

import math
import re
import requests
from bs4 import BeautifulSoup, NavigableString
#from PyKomoran import *
from konlpy.tag import *
from nltk import word_tokenize
import datetime

word_d = {}

def hfilter(s):
#	return re.sub(u'[^ \.\,\?\!\u0041-\u005A\u0061-\u007A\uac00-\ud7a3]+','',s)
	return re.sub(u'[^ \.\,\?\!\uac00-\ud7a3]+','',s)

def compute_tf(s):
	'''	
	bow = set()
	# dictionary for words in the given sentence (document)
	wordcount_d = {}
	
	tokenized = word_tokenize(s)
	for tok in tokenized:
		if tok not in wordcount_d.keys():
			wordcount_d[tok]=0
		wordcount_d[tok] += 1
		bow.add(tok)
	'''
	tf_d = {}
	for word,count in word_d.items():
		tf_d[word] = count / float(len(word_d))

	return tf_d

def compute_idf():
#	Dval = len(sent_list)
	Dval = len(word_d)
	# build set of words
	'''	
	bow = set()
	for i in range(0, len(sent_list)):
		tokenized = word_tokenize(sent_list[i])
		for tok in tokenized:
			bow.add(tok)
	'''
	idf_d = {}
	for t in word_d:
		cnt = 0
		for s in sent_list:
			if t in word_tokenize(s):
				cnt += 1
		idf_d[t] = math.log(Dval/float(cnt))

	return idf_d

if __name__ == '__main__':
	now = datetime.datetime.now()
	newslink = []
	newstitle = []
	texttemp = []
	textlist = []
	sent_list = []
	wlist = {}
	
	mecab = Mecab()
	for i in range(1):#오늘 많이 본 기사 링크 끌어오기
		datestr = now.strftime('%Y%m%d')
		url = 'https://finance.naver.com/news/news_list.nhn?mode=RANK&date=' + datestr
		res = requests.get(url)
		html = BeautifulSoup(res.content, 'html.parser')
		newslist = html.find_all(attrs={'class':'simpleNewsList'})
		for j in newslist:
			newslist2 = j.find_all('a')
			for k in newslist2:
				newslink.append(k['href'])
#				newstitle.append(k['title'])
#		print(newstitle)
		for j in newslink:
			newsurl = 'https://finance.naver.com' + j
			newsres = requests.get(newsurl)
			newshtml = BeautifulSoup(newsres.content, 'html.parser')
			content = newshtml.find(attrs={'class':'articleCont'})
			content.find("div").extract()
			textlist.append(hfilter(content.text).split('.'))

		for j in textlist:
			for k in j:
				hsent = hfilter(k)
				wlist = mecab.nouns(hsent)
				for w in wlist:
					mw = mecab.pos(w)
					if w not in word_d and mw[0][1] == "NNP":
						word_d[w] = 0
						sent_list.append(w)
					elif mw[0][1] == "NNP":
						word_d[w] += 1
#		print(word_d)
		
		temp = {}

		idf_d = compute_idf()

		for j in sent_list:
			tf_d = compute_tf(j)
			for word,tfval in tf_d.items():
				temp[word] = tfval*idf_d[word]
		
		important_word = {}
		wordsave = []
		
		for w,c in sorted(temp.items(), key=lambda x:x[1], reverse=True):
			if len(w) >= 3:
				important_word[w] = c
				wordsave.append(w)
		icnt = 0
		for w,c in important_word.items():
			if icnt == 10:
				break
			else:
				icnt += 1
				print(w,c)
		now = now - datetime.timedelta(1)
