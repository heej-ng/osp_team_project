#!/usr/bin/python3
#-*- coding: utf-8 -*-

import re
import requests
import argparse
import subprocess
from flask import Flask, jsonify, request
from flask import render_template
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route('/')
def popular():
	url = u'https://finance.naver.com/sise/lastsearch2.nhn'
	res = requests.get(url)
	html = BeautifulSoup(res.content, "html.parser")
	html_table = html.find(class_="type_5")
	html_list = html_table.find_all("a", limit=15)
	list=[]
	for x in html_list:
	    list.append(x.text)
	return render_template('index.html', p0=list[0], p1=list[1], p2=list[2], p3=list[3], p4=list[4], p5=list[5], p6=list[6], p7=list[7], p8=list[8], p9=list[9], p10=list[10], p11=list[11], p12=list[12], p13=list[13], p14=list[14])

if __name__ == '__main__':
    ipaddr="127.0.0.1"
    app.run(debug=False, host=ipaddr, port=5000)

