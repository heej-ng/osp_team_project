#!/usr/bin/python

import math
import re
import requests
from bs4 import BeautifulSoup, NavigableString
from konlpy.tag import Twitter
from konlpy.tag import Okt
from PyKomoran import *
from konlpy.tag import *
from nltk import word_tokenize

word_d = {}
resultword = {}
sent_list = []

def hfilter(s):
	return re.sub(u'[^ \.\,\?\!\u3130-\u318f\uac00-\ud7a3]+','',s)

def process_new_sentence(s):
	sent_list.append(s)
	tokenized = word_tokenize(s)
	for word in tokenized:
		if word not in resultword.keys():
			resultword[word]=0
		resultword[word] += 1

def compute_tf(s):
	bow = set()
	# dictionary for words in the given sentence (document)
	wordcount_d = {}
	
	tokenized = word_tokenize(s)
	for tok in tokenized:
		if tok not in wordcount_d.keys():
			wordcount_d[tok]=0
		wordcount_d[tok] += 1
		bow.add(tok)

	tf_d = {}
	for word,count in wordcount_d.items():
		tf_d[word] = count / float(len(bow))

	return tf_d

def compute_idf():
#	Dval = len(sent_list)
	Dval = len(word_d)
	# build set of words
	bow = set()

	for i in range(0, len(sent_list)):
		tokenized = word_tokenize(sent_list[i])
		for tok in tokenized:
			bow.add(tok)

	idf_d = {}
	for t in bow:
		cnt = 0
		for s in sent_list:
			if t in word_tokenize(s):
				cnt += 1
		idf_d[t] = math.log(Dval/float(cnt))

	return idf_d

if __name__ == '__main__':

#	twitter = Twitter()
#	okt = Okt()
#	hannanum = Hannanum()
	mecab = Mecab()
#	komoran = Komoran()

	url1 = u'https://finance.naver.com/news/news_read.nhn?article_id=0004652748&office_id=014&mode=RANK&typ=0'
	url2 = u'https://finance.naver.com/news/news_read.nhn?article_id=0004923082&office_id=277&mode=RANK&typ=0'
	url3 = u'https://finance.naver.com/news/news_read.nhn?article_id=0000001844&office_id=648&mode=RANK&typ=0'
	url4 = u'https://finance.naver.com/news/news_read.nhn?article_id=0004660036&office_id=014&mode=RANK&typ=0'
	url5 = u'https://finance.naver.com/news/news_read.nhn?article_id=0000706150&office_id=417&mode=RANK&typ=0'
	url6 = u'https://finance.naver.com/news/news_read.nhn?article_id=0004962515&office_id=018&mode=RANK&typ=0'

	ulist = [url1, url2, url3, url4, url5, url6]
	res = []
	for i in range(0, len(ulist)):
		res.append(requests.get(ulist[i]))
	
	html = []
	for i in range(0, len(ulist)):
		html.append(BeautifulSoup(res[i].content, "html.parser"))

	html_project = []
	for i in range(0, len(ulist)):
		html_project.append(html[i].find(attrs={'id':'content'}))

	for i in range(0, len(ulist)):
		html_project[i].find("div").extract()

	html_text = []
	for i in range(0, len(ulist)):
		html_text.append(html_project[i].text)

	result = []
	for i in range(0, len(ulist)):
		result.append(hfilter(html_text[i]))

	textlist = []
	for i in range(0, len(ulist)):
		textlist.append(result[i].split('.'))

	wlist = {}
	for num in range(0, len(textlist)):
		for t in textlist[num]:
			hsent = hfilter(t)
#			wlist = twitter.nouns(hsent)
#			wlist = okt.nouns(hsent)
			wlist = mecab.nouns(hsent) # NNG보다 NNP 추출 해보기
#			print(wlist)
			for i in range(0,len(wlist)):
#				process_new_sentence(wlist[i])
				sent_list.append(wlist[i])
			for w in wlist:
				mw = mecab.pos(hsent)
				if w not in word_d:
					word_d[w] = 0
				elif mw[1] == "NNP":
					word_d[w] += 1
			'''
			for w in wlist:
				if w not in word_d:
					word_d[w] = 0
				else:
					word_d[w] += 1
			'''
	temp = {}

	idf_d = compute_idf()
	
	for i in range(0, len(sent_list)):
		tf_d = compute_tf(sent_list[i])
		for word,tfval in tf_d.items():
			temp[word] = tfval*idf_d[word]
	
	important_word = {}
	wordsave = []
	
	for w,c in sorted(temp.items(), key=lambda x:x[1], reverse=True):
		if len(w) >= 2:
			important_word[w] = c
			wordsave.append(w)
	
	for i in range(0, len(wordsave)):
		print(mecab.pos(wordsave[i]))

	icnt = 0
	for w,c in important_word.items():
		if icnt == 10:
			break
		else:
			icnt += 1
			print(w,c)

