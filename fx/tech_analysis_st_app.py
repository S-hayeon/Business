#%pip install --upgrade pip
import datetime
import matplotlib.pyplot as plt
import numpy as np
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
