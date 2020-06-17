import requests
import csv
from bs4 import BeautifulSoup
import pandas as pd
import json
import pandas as pd
import datetime
import json
import re
import datetime
import time

def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
    return BeautifulSoup(requests.get(url=url, headers=headers).content, "html.parser")
    


def get_shop_list(api = "dy8fex63879fnclp7em1j90i"):
    shop_list = []
      
    #"limit" attribute to expand records from default 25 to 100 shops
    #facemask shop number is about around 700
    for i in range(8):
        offset = i * 100
        site = 'https://openapi.etsy.com/v2/shops?limit=100&offset=%f&shop_name=face*mask&api_key=%s'%(offset,api )
        webpage = requests.get(site)
        shop_json = json.loads(webpage.text)
    
        for s in shop_json['results']:
            shop_list.append((s['shop_id'], s['shop_name'],
                              s["currency_code"],s['listing_active_count']))
    return shop_list


def get_product_info(shoplist, api = 'dy8fex63879fnclp7em1j90i'):
    shoplist_ = shoplist
    shop_output = {}
    time.sleep(1)
    
    for i,shop in enumerate(shoplist_):
        if i%5 ==0: 
            time.sleep(0.2) #api limit 5 times per second
            
        shopId, title, currency, listing_active_count = shop[0],shop[1],shop[2], shop[3]
        shop_output[shopId]={}
        shop_output[shopId]['title'] = title
        shop_output[shopId]['currency'] = currency
        
        #extract active listing products from each shop
        #just consider first 100 products
        url = 'https://openapi.etsy.com/v2/shops/%f/listings/active?limit=100&api_key=%s'%(shopId,api)
        listing = requests.get(url)
        listing_json = json.loads(listing.text)
        
        #get listing product info
        shop_output[shopId]['listing'] = {}
        price_favorer = 0
        total_favorer = 0
        p = 0
        for product in listing_json['results']:
            listing_id = product['listing_id']
            shop_output[shopId]['listing'][listing_id] = {}
            price = float(product['price'].replace(",",''))
            shop_output[shopId]['listing'][listing_id]['price'] = price
            shop_output[shopId]['listing'][listing_id]['num_favorers'] = product['num_favorers']
            shop_output[shopId]['listing'][listing_id]['quantity'] = product['quantity']
            price_favorer += price * product['num_favorers']
            total_favorer += product['num_favorers']
            p += price
        
        #Avg Price
        try:
            avg_price =  price_favorer / total_favorer
        except ZeroDivisionError:
            try:
                avg_price = p / listing_active_count
            except ZeroDivisionError:
                avg_price = 0
        shop_output[shopId]['avg_price'] = avg_price
        #shop average price weighted by number of product favorer
        
        
        #get shop historical sales
        shop_web = 'https://www.etsy.com/shop/%s?ref=ss_profile'%shop_output[shopId]['title']
        soup = get_html(shop_web)
        try:
            sale = soup.find('span', attrs = {'class':'shop-sales hide-border no-wrap'})
        except KeyError:
            print(shop_web)
            continue
        try:
            sales = float(sale.text.replace(' Sales','').replace(',','').replace(' Sale',''))
            shop_output[shopId]['sale'] = sales 
        except AttributeError:
            shop_output[shopId]['sale'] = 0
            
    return shop_output



shop_list = get_shop_list(api = 'dy8fex63879fnclp7em1j90i')
output = get_product_info(shop_list)
d = datetime.datetime.now().strftime('%Y-%m-%d')
with open('/Users/xiaojing/Documents/Jingxiao/RealTimeBigData_3Tasks/Task3/%s.json'%d, 'w') as f:
    json.dump(output, f)