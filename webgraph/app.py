# 그래프를 그리는 app.py

#!/usr/bin/python3
#-*- coding: utf-8 -*-

import argparse
import subprocess
import FinanceDataReader as fdr
import pandas as pd
from flask import Flask, send_file, jsonify, request
from flask import render_template
from io import StringIO, BytesIO
import numpy as np

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

#################################################

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
	return render_template('mainpage.html')

#여기로 들어가면 그림이 나옴.
@app.route('/images/<stock>')
def images(stock):
    return render_template("images.html", title=stock)

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
        #print(df_krx)
        df_name = df_krx[df_krx['Name'] == val]
        symbol = df_name.iloc[0, 0]
        name = df_name.iloc[0, 2]

    return symbol, name

#print(stock_code('대한전선'))
#print(stock_code('쌍방울'))

@app.route('/fig/<stock>')
def fig(stock):
    # print("fig!!!!!!!!!!!!!!!!!!!!!!!!!!!!!hi")

    #title = stock_code('카카오')[1] + '(' + stock_code('카카오')[0] + ')'
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
    pr_line = plt.subplot2grid((4, 4), (0, 0), rowspan=3, colspan=4,)
    #vol_bar = plt.subplot2grid((4, 4), (3, 0), rowspan=1, colspan=4)
    x = chart.index.strftime('%m.%d')

    pr_line.plot(chart.index, chart['5일'], label='MA5')
    pr_line.plot(chart.index, chart['20일'], label='MA20')
    pr_line.plot(chart.index, chart['60일'], label='MA60')
    pr_line.plot(chart.index, chart['120일'], label='MA120', color='purple')
    pr_line.bar(chart.index, height= chart['Close'] - chart['Open'], bottom=chart['Open'], width=1, color= list(map(lambda c: 'red' if c>0 else 'blue', chart['Change'])))
    pr_line.vlines(chart.index, chart['Low'], chart['High'], color= list(map(lambda c: 'red' if c>0 else 'blue', chart['Change'])))

    # vol_bar.bar(x, df['Volume'])
    #plt.show()
    #print(fig)

    img = BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
	ipaddr="127.0.0.1"
	app.run(debug=False, host=ipaddr, port=5000)
