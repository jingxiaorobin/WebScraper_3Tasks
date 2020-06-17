import pandas as pd
import re
import datetime
import time
import selenium
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

c_list = ['USD', 'GBP', 'HKD', 'CAD', 'EUR', 'SEK', 'CHF', 'NZD', 'AUD']

currency = []
for c in c_list:
    link = 'https://widget-yahoo.ofx.com/?base=%s&term=USD'%c
    opts = Options()
    opts.headless = True
    chromepath = '/usr/local/bin/chromedriver'
    browser = Chrome(chromepath, options=opts)
    browser.implicitly_wait(1)
    
    browser.get(link)
    time.sleep(2)
    value = browser.find_element_by_class_name('title-to-price').text
    browser.close()
    currency.append(value)
    

d = datetime.datetime.now().strftime('%Y-%m-%d')
currency.append(d)
path = '/Users/xiaojing/Documents/Jingxiao/RealTimeBigData_3Tasks/Task3/'
with open(path + 'currency.csv','a') as f:
    f.write(",".join(currency))
    f.write('\n')
f.close()

