# This .py web scrapeing the commercial flight number historicial data for past 120 days from website flightradar24.com.

import requests
import csv
from bs4 import BeautifulSoup
import pandas as pd
import json
import pandas as pd
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

commercial_7d = chart_json['commercial']['series'][0]['data']
commercial_num = chart_json['commercial']['series'][1]['data']

#Merge two list to a dataframe, change timestamp to date
df = pd.DataFrame(commercial_7d,columns=['Date',\
                                         'Commercial Flight 7-Day Moving Avg'],\
                                          index=None)
df['Number of Commercial Flight'] = [i[1] for i in commercial_num]
df.sort_values(by=['Date'], inplace = True)
df['Date'] = pd.to_datetime(df.Date, unit='ms') #Change timestamp to datetime
#Write to csv
df.to_csv('Flight.csv',index=None)