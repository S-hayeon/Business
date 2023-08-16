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
import yfinance as yf
#c=np.random.randn(100)
#macd=trend.MACD(close=c,window_slow=26,window_fast=12,window_sign=9)
################ Session State Variables ###############################################################################################################
if "CurrencyPair" not in st.session_state:
  st.session_state["CurrencyPair"]=""
if "Symbol" not in st.session_state:
  st.session_state["Symbol"]=""
if "Interval" not in st.session_state:
  st.session_state["Interval"]=""
if "StartDate" not in st.session_state:
  st.session_state["StartDate"]=""
if "EndDate" not in st.session_state:
  st.session_state["EndDate"]=""

################ Sidebar ###############################################################################################################
currencypair=st.sidebar.selectbox("Select you investment currency pair: ",main.maj_forex_pairs)
st.session_state["CurrencyPair"]=currencypair
cur_symbol=f"{currencypair}=X"
st.session_state["Symbol"]=cur_symbol
ticker=yf.Ticker(st.session_state["Symbol"])
# Create the select slider
selected_interval = st.sidebar.select_slider('Select an interval:', options=main.labels)
# Map the selected value to the corresponding interval
#selected_value = main.intervals[selected_interval]
# Map the selected label to the corresponding interval
selected_value = main.intervals[main.labels.index(selected_interval)]
st.session_state["Interval"]=selected_value
#data = main.collect_forex_data(f"{currencypair}=X",selected_value)
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"))
st.session_state["StartDate"]=start_date
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2023-08-01"))
st.session_state["EndDate"]=end_date
##########################################################################################################################################

################ Ticker Information ###############################################################################################################
tickerInfo=pd.DataFrame(ticker.info.items(),columns=['Parameter','Value'])
tickerInfo[tickerInfo['Value']!=0].dropna() # Drop values where Value Column is equal to 0 then drop Nan/None values
tickerInfo_expander=st.empty()
with tickerInfo_expander.expander("FX Asset Information"):
  st.dataframe(tickerInfo)
st.write(f"Investment yako ya {currencypair} inabamba enyewe")
################ Historical and Real Time Data Table ###############################################################################################################
data=ticker.history(interval=st.session_state["Interval"],start=start_date, end=end_date)
data=data.reset_index() # Reset Datetime index
#data=data[data['Open','High','Low','Close']]
timezone=st.sidebar.selectbox("Select your Timezone: ",main.timezones)
data=data.index.tz_convert(timezone)
tickerData_expander=st.empty()
with tickerData_expander.expander(" OHLC Candlestick Fx Data"):
  st.dataframe(data)
#ta=TIndicators(data['Open'])
#results=ta.MACD()
#st.write(results)
#st.write(data)

