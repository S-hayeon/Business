!pip install --upgrade pip
import datetime
import matplotlib.pyplot as plt
import MetaTrader5 as mt5
import numpy as np
import os
os.system("bash /app/path/to/setup.sh")
import pandas as pd
import streamlit as st
try:
  import sys
  #from ta import trend
  #sys.path.append('/app/business/fx')
  sys.path.append('/app/business')
  from fx import main
except:
  import sys
  sys.path.append('/mount/src/business')
  from fx import main

from technical_analysis import TIndicators
mt5.initialize()
#c=np.random.randn(100)
#macd=trend.MACD(close=c,window_slow=26,window_fast=12,window_sign=9)
if "CurrencyPair" not in st.session_state:
  st.session_state["CurrencyPair"]=""
currencypair=st.selectbox("Select you investment currency pair: ",main.maj_forex_pairs)
st.session_state["CurrencyPair"]=currencypair
years = [2001, 2002, 2003, 2004, 2005,
        2006, 2007, 2008, 2009, 2010,
        2011, 2012, 2013, 2014, 2015,
        2016, 2017, 2018, 2019, 2020,
        2021]

months = [1, 2, 3, 4, 5, 6,
         7, 8, 9, 10, 11, 12]

timeframes = {
    'W1' : 1  | 0x8000,
    'MN1': 1  | 0xC000
}        

    
for year in years:
    for month in months:
        for timeframe in timeframes:
            # request tick data
            if month != 12:
                ticks = mt5.copy_rates_range(
                    'WIN$N', 
                    timeframes[timeframe], 
                    datetime(year, month, 1), 
                    datetime(year, month + timedelta(month=1), 1)
                )
                ticks = pd.DataFrame(ticks)
            else:
                ticks = mt5.copy_rates_range(
                    'WIN$N', 
                    timeframes[timeframe], 
                    datetime(year, month, 1), 
                    datetime(year, month, calendar.monthrange(ano,mes)[1])
                )
                ticks = pd.DataFrame(ticks)
st.dataframe(ticks)
#st.write(results)
#selected_interval = st.slider('Select an interval:', 0, len(main.intervals)-1, format_func=lambda i: main.labels[i])

# Create the select slider
selected_interval = st.select_slider('Select an interval:', options=main.labels)

# Map the selected value to the corresponding interval
#selected_value = main.intervals[selected_interval]
# Map the selected label to the corresponding interval
selected_value = main.intervals[main.labels.index(selected_interval)]
data = main.collect_forex_data(f"{currencypair}=X",selected_value)
#data = main.collect_forex_data(f"{currencypair}=X",selected_interval)
ta=TIndicators(data['Open'])
results=ta.MACD()
st.write(results)
#st.write(data)
st.write(f"Investment yako inabamba enyewe {currencypair}")
