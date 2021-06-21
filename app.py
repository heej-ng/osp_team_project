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
from fdr_test import graph

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
#################################################

app = Flask(__name__)

# @app.route('/', methods=['GET'])
# def home():
# 	return render_template('mainpage.html')

#여기로 들어가면 그림이 나옴.
@app.route('/images/<cropzonekey>')
def images(cropzonekey):
    print("images!!!!!!!!!!!!!!!!!!!!!!!!!!!!!hi")
    return render_template("images.html", title=cropzonekey)

@app.route('/fig/<cropzonekey>')
def fig(cropzonekey):
    # print("fig!!!!!!!!!!!!!!!!!!!!!!!!!!!!!hi")
    # #fig = plt.figure(figsize=(15, 10))
    # img = graph('005930')
    # # img = StringIO()
    # # fig.savefig(img)
    # # img.seek(0)
    # plt.show()

    df = fdr.DataReader('005930', '2019')
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
