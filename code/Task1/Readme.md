# Task A: Daily Flights
## 1. Go to the website below:
> https://www.flightradar24.com/data/statistics

+ Flight_Hist_Data.py extracts historical 120 daily commercial flight data and saves in Flight.csv
+ Flight_Daily.py extracts new daily data and append to the Flight.csv
+ Automation run Flight_Daily.py at 9pm each day
> $cronbat -e
> * 21 * * * root/bin/python3 path/to/Flight_Daily.py

+ Visualization:
