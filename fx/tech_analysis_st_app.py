#%pip install --upgrade pip
import datetime
import matplotlib.pyplot as plt
import numpy as np
import os
#/home/adminuser/venv/bin/python -m pip install --upgrade pip
os.system("bash /mount/src/business/fx/setup.sh")
#import MetaTrader5 as mt5
import mt5
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
import time
#c=np.random.randn(100)
#macd=trend.MACD(close=c,window_slow=26,window_fast=12,window_sign=9)
if "CurrencyPair" not in st.session_state:
  st.session_state["CurrencyPair"]=""
currencypair=st.selectbox("Select you investment currency pair: ",main.maj_forex_pairs)
st.session_state["CurrencyPair"]=currencypair
import mt5
# Create a connection to the MT5 server
mt5.initialize()
fetchDataMode=st.selectbox("Select Data Fetch: ",['Historical','Real-Time'])
if fetchDataMode=='Historical':
  ticks = mt5.copy_ticks_from(currencypair, mt5.TIMEFRAME_D1, datetime(2023, 1, 1), datetime(2023, 7, 31)) # Get the historical tick data for the EURUSD symbol from 2023-01-01 to 2023-07-31
elif fetchDataMode=='Real-Time':
  #ticks=mt5.subscribe_to_market_data(currencypair) # Subscribe to the real time ticks data for the EURUSD symbol
  # Get the latest tick data
  ticks = mt5.get_last_tick("EURUSD")
  # Print the tick data
  #time.sleep(1)
else:
  pass
ticks=pd.DataFrame(ticks)
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
