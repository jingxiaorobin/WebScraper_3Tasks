# Masks Sold by Etsy
The project goal is to estimate daily sales data face mask from Etsy. The code automatically extract via
> Mask.py
    currency.py

export daily sale data to
> 2020-06-xx.csv]
    currency.csv
    
Aggregated dataset:
> Etsy_Mask_sale.csv


### Method:
1. Get Etsy APIkey
2. Extract all the shops(shopId), whose names contain 'face' and 'mask', from Etsy developer
3. For each face mask shop, extract historical sales, each listing product price, each  product favor number, shopId
4. Calculate weighted average price for each shop
5. Calculate daily product sale by Day2 historical sale deducting Day1 historical sale
6. Function:

Revenue_{day2} = \sum \bar{p}  \, \cdot \, (q_{day2} \, -\, q_{day1})\, \cdot \, \$ \, rate

### Preliminary data process and data aggregation
> Etsy_mask.ipynb