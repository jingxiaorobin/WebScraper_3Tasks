#Urber pricing- extract price for Pool, UberX, WAV, UberXL, Car Seat, Black and Black SUV start to stop

import selenium
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime

p = {"URL":"https://www.uber.com/us/en/price-estimate",
     "box1":"pickup","box2":"destination",
     "box3":'View all options',
    "trip_price":"//div[@role='radiogroup']",
    "view":"//div/button[@aria-label=\"View all options\"]"} #parameter



def uber_scraper(start,stop,browser):
   
    browser.get(p["URL"])
    time.sleep(5)
    start_field = browser.find_element_by_name(p['box1'])
    start_field.send_keys(start)
    WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.TAG_NAME, "li"))
    )
    time.sleep(5)
    start_field.send_keys(Keys.RETURN)
    
    
    end_field = browser.find_element_by_name(p['box2'])
    end_field.send_keys(stop)
    WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.TAG_NAME, "li"))
    )
    time.sleep(5)
    end_field.send_keys(Keys.RETURN)
    
    XPATH = p['trip_price'] # unique radiogroup buttons
    WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, XPATH)))
    time.sleep(5)
    
    view = p['view']
    view_all = browser.find_element_by_xpath(view)
    view_all.click()
    time.sleep(5)
    tags = browser.find_elements_by_xpath(XPATH)
    return tags

def parse(tags):
    out = {}
    tag = tags[0].text
    tag = tag.replace("$","")
    tag = tag.split('\n')
    for i in range(0,len(tag)-1,2):
        out[tag[i]] = tag[i+1]
    return out


    
def serial_scraper(start_coded,stop_coded,kind = 'uber'):
    opts = Options()
    opts.headless = True
    chromepath = '/usr/local/bin/chromedriver'
    browser = Chrome(chromepath, options=opts)
    browser.implicitly_wait(0)
    
    try:
        tags = uber_scraper(start_coded,stop_coded, browser)
        out = parse(tags)
    except:
        tags = None
        out = None
       
    browser.close()
    return out
    
    
    
    
start_coded = 'Grand Central Terminal, 89 E 42nd St, New York, NY'
stops = ['World Trade Center, New York, NY',
              'John F. Kennedy International Airport, Queens, NY',
              'Citi Field, 41 Seaver Way, Queens, NY']
time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


for stop_coded in stops:
    trip_price = serial_scraper(start_coded,stop_coded,kind = 'uber')
    try:
        value = list(trip_price.values())
    except AttributeError:
        try:
            time.sleep(5)
            value = list(trip_price.values())
        except AttributeError:
            value = [0] * 7
            pass
    value = value + ['Grand Central',stop_coded.replace(',',''),time_now]
    with open('/Users/xiaojing/Documents/Jingxiao/RealTimeBigData_3Tasks/Task2/uber.csv','a') as file:
        file.write(','.join(value))
        file.write('\n')
    file.close()
    