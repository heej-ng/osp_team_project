#!/usr/bin/python3
#-*- coding: utf-8 -*-

import argparse
import subprocess
from flask import Flask, jsonify, request
from flask import render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
	return render_template('mainpage.html')

if __name__ == '__main__':
	ipaddr="127.0.0.1"
	app.run(debug=False, host=ipaddr, port=5000)
