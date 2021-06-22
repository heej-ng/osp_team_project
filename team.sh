#!/bin/bash

pip3 install requests
pip3 install beautifulsoup4
pip3 install konlpy
pip3 install datetime
pip3 install -U finance_datareader
pip3 install pandas
pip3 install matplotlib

cd
cd elasticsearch-7.6.2
./bin/elasticsearch -d
cd
cd osp_team_project-main

chmod +x app.py
python3 app.py
