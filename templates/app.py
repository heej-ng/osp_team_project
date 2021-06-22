#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import requests
import argparse
import subprocess
import FinanceDataReader as fdr
import pandas as pd
from flask import Flask, send_file, jsonify, request
from flask import render_template
from io import StringIO, BytesIO
import numpy as np
from bs4 import BeautifulSoup

import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt

##############################################

app = Flask(__name__)


@app.route('/')
def popular():
    url = u'https://finance.naver.com/sise/lastsearch2.nhn'
    res = requests.get(url)
    html = BeautifulSoup(res.content, "html.parser")
    html_table = html.find(class_="type_5")
    html_list = html_table.find_all("a", limit=15)
    list = []
    for x in html_list:
        list.append(x.text)
    return render_template('index.html', p0=list[0], p1=list[1], p2=list[2], p3=list[3], p4=list[4], p5=list[5],
                           p6=list[6], p7=list[7], p8=list[8], p9=list[9], p10=list[10], p11=list[11], p12=list[12],
                           p13=list[13], p14=list[14])


@app.route('/detail/<stock>')
def detail(stock):
    url = 'https://finance.naver.com/item/main.nhn?code={}'.format(stock_code(stock)[0])
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")

    # 주가, 전일대비, 거래량, 거래대금, 시가총액, 시가총액순위
    # 주가
    s1 = soup.find(class_="no_up").find(class_="blind").text

    #전일대비
    s2 = soup.find(class_="no_exday").find_all(class_="no_up")  # .find(class_="blind") ##.find(class_="no_up").
    s2 = s2[1].get_text().split()
    s2 = s2[0] + s2[1] + s2[3]

    trade = soup.find(class_="no_info").find_all(class_="blind")
    #거래량
    s3 = trade[3].get_text()
    #거래대금
    s4 = trade[6].get_text()

    siga = soup.find_all(class_="first")
    siga = siga[3].get_text().split()
    #시가총액
    s5 = siga[2] + ' ' + siga[3] + siga[4]
    #시가총액순위
    s6 = siga[6] + ' ' + siga[7]

    return render_template("detail.html", title=stock, d1=s1, d2=s2, d3=s3, d4=s4, d5=s5, d6=s6)


# 한글, 영어 구분; 한글 -> 'k', 영어 ->'e'
def isEnglishOrKorean(input_s):
    k_count = 0
    e_count = 0
    for c in input_s:
        if ord('가') <= ord(c) <= ord('힣'):
            k_count += 1
        elif ord('a') <= ord(c.lower()) <= ord('z'):
            e_count += 1
    return "k" if k_count > 1 else "e"


# 한국기업은 기업명, 미국기업은 티커 입력 -> symbol, name
def stock_code(val):
    if isEnglishOrKorean(val) == 'e':
        df_nsq = fdr.StockListing('LASDAQ')
        df_nyse = fdr.StockListing('NYSE')
        df_us = pd.concat([df_nsq, df_nyse])
        df_name = df_us[df_us['Symbol'] == val]
        symbol = df_name.iloc[0, 0]
        name = df_name.iloc[0, 1]
    else:
        df_krx = fdr.StockListing('KRX')
        # print(df_krx)
        df_name = df_krx[df_krx['Name'] == val]
        symbol = df_name.iloc[0, 0]
        name = df_name.iloc[0, 2]

    return symbol, name


@app.route('/fig/<stock>')
def fig(stock):
    # print("fig!!!!!!!!!!!!!!!!!!!!!!!!!!!!!hi")

    # title = stock_code('카카오')[1] + '(' + stock_code('카카오')[0] + ')'
    df = fdr.DataReader(stock_code(stock)[0], '2019')
    print(df)
    df['Close'].plot()

    chart = df

    ma5 = pd.DataFrame(chart['Close'].rolling(window=5).mean())
    ma20 = pd.DataFrame(chart['Close'].rolling(window=20).mean())
    ma60 = pd.DataFrame(chart['Close'].rolling(window=60).mean())
    ma120 = pd.DataFrame(chart['Close'].rolling(window=120).mean())
    chart.insert(len(chart.columns), '5일', ma5)
    chart.insert(len(chart.columns), '20일', ma20)
    chart.insert(len(chart.columns), '60일', ma60)
    chart.insert(len(chart.columns), '120일', ma120)

    fig = plt.figure(figsize=(15, 10))
    pr_line = plt.subplot2grid((4, 4), (0, 0), rowspan=3, colspan=4, )
    # vol_bar = plt.subplot2grid((4, 4), (3, 0), rowspan=1, colspan=4)
    x = chart.index.strftime('%m.%d')

    pr_line.plot(chart.index, chart['5일'], label='MA5')
    pr_line.plot(chart.index, chart['20일'], label='MA20')
    pr_line.plot(chart.index, chart['60일'], label='MA60')
    pr_line.plot(chart.index, chart['120일'], label='MA120', color='purple')
    pr_line.bar(chart.index, height=chart['Close'] - chart['Open'], bottom=chart['Open'], width=1,
                color=list(map(lambda c: 'red' if c > 0 else 'blue', chart['Change'])))
    pr_line.vlines(chart.index, chart['Low'], chart['High'],
                   color=list(map(lambda c: 'red' if c > 0 else 'blue', chart['Change'])))

    # vol_bar.bar(x, df['Volume'])
    # plt.show()
    # print(fig)

    img = BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')


if __name__ == '__main__':
    ipaddr = "127.0.0.1"
    app.run(debug=False, host=ipaddr, port=5000)
