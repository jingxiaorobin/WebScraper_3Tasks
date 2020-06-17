# This .py web scrapeing the commercial flight number daily data from flightradar24.com.
import requests
import csv
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import datetime


def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
    return BeautifulSoup(requests.get(url=url, headers=headers).content, "html.parser")


site = 'https://www.flightradar24.com/data/statistics'
page = get_html(site)

#Find two lists --- Commercial Flight 7 Day MA, Commercial Flight No.
chart = page.find_all('script', attrs={'type':"text/javascript"})
chart_str = chart[1].text.split('var charts = ')[1].split(";")[0]
chart_json = json.loads(chart[1].text.split('var charts = ')[1].split(";")[0])

commercial_7d = chart_json['commercial']['series'][0]['data'][0] #Latest data come the first
commercial_num = chart_json['commercial']['series'][1]['data'][0]#Latest data come the first

commercial_7d[0] = str(datetime.fromtimestamp(commercial_7d[0]/1000+3600*24).strftime('%Y-%m-%d'))
with open('/Users/xiaojing/Documents/Jingxiao/RealTimeBigData_3Tasks/Task1/Flight.csv', 'a') as file:
    file.write('\n')
    file.write(','.join([str(commercial_7d[0]),str(commercial_7d[1]),str(commercial_num[1])]))
file.close()