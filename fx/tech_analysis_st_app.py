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
if "EndDate" not in st.session_state:
  st.session_state["EndDate"]=""
if "Interval" not in st.session_state:
  st.session_state["Interval"]=""
if "StartDate" not in st.session_state:
  st.session_state["StartDate"]=""
if "Symbol" not in st.session_state:
  st.session_state["Symbol"]=""
if "Timezone" not in st.session_state:
  st.session_state["Timezone"]=""

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
timezone=st.sidebar.selectbox("Select your Timezone: ",main.timezones)
##########################################################################################################################################
def get_forex_change(symbol):
    forex_pair = yf.Ticker(symbol)
    history = forex_pair.history(interval='1d')
    if len(history) < 2:
        return None
    previous_close = history['Close'][-2]
    current_close = history['Close'][-1]
    change = ((current_close - previous_close) / previous_close) * 100
    return [current_close,change]
forex_pairs = [
        "EURUSD=X",  # Euro to US Dollar
        "USDJPY=X",  # US Dollar to Japanese Yen
        "GBPUSD=X",  # British Pound to US Dollar
        "USDCHF=X",  # US Dollar to Swiss Franc
        "AUDUSD=X",  # Australian Dollar to US Dollar
        "USDCAD=X",  # US Dollar to Canadian Dollar
        "NZDUSD=X",  # New Zealand Dollar to US Dollar
    ]
col1, col2, col3 = st.columns(3)
forex_pairs = ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "AUDUSD=X", "USDCAD=X", "NZDUSD=X"]
for index,currency in enumerate(forex_pairs):
    if index % 3 == 0:
        col = col1
    elif index % 3 == 1:
        col = col2
    else:
        col = col3
    with col:
        currency_value = get_forex_change(currency)  # Assuming you have a function to get forex values
        st.metric(label=currency.replace("=X", ""), value=currency_value[0], delta=currency_value[1])

################ Ticker Information ###############################################################################################################
tickerInfo=pd.DataFrame(ticker.info.items(),columns=['Parameter','Value'])
tickerInfo[tickerInfo['Value']!=0].dropna() # Drop values where Value Column is equal to 0 then drop Nan/None values
if st.session_state["Symbol"] != '':
  tickerInfo_expander=st.empty()
  with tickerInfo_expander.expander("FX Asset Information"):
    st.dataframe(tickerInfo)
st.write(f"Investment yako ya {currencypair} inabamba enyewe")
################ Historical and Real Time Data Table ###############################################################################################################
#if st.session_state["StartDate"] !=  '' and st.session_state["EndDate"] !=  '' and st.session_state["Timezone"] !=  '' :
tickerData_expander=st.empty()
with tickerData_expander.expander(" OHLC Candlestick Fx Data"):
  data=pd.DataFrame(ticker.history(interval=st.session_state["Interval"],start=st.session_state["StartDate"], end=st.session_state["EndDate"]))
  data.index=data.index.tz_convert(timezone)
  data=data.reset_index() # Reset Datetime index
  data = data.loc[:, (data != 0).any(axis=0)] # Drop columns with all zero values
  #st.write(f'The columns are: {data.columns}')
  st.dataframe(data)
#ta=TIndicators(data['Open'])
#results=ta.MACD()
#st.write(results)
#st.write(data)

