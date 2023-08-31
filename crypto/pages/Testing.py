import pandas as pd
import pandas_ta as ta
import streamlit as st
strategies=['VWAP_Bollinger_RSI','None']
strategy=st.selectbox("My preferred Strategy is",strategies)
if strategy=='VWAP_Bollinger_RSI':
  prevCandles=st.sidebar.number_input("No of Previous candles",min_value=3,step=1)
  bollPeriod=st.sidebar.number_input("Bollinger Bands Time period",min_value=2,step=1)
  bollDev=st.sidebar.number_input("Bollinger Bands Standard Deviation",min_value=1,step=1)
  rsiPeriod=st.sidebar.number_input("RSI Time period",min_value=2,step=1)
  rsi_buyThreshold=st.sidebar.number_input("RSI Buy Threshold",min_value=5,step=1)
  rsi_sellThreshold=st.sidebar.number_input("RSI Sell Threshold",min_value=rsi_buyThreshold,step=1)
  sl_co_efficient=st.sidebar.number_input("Stop Loss Co-efficient",min_value=0.1,step=0.01)
  tp_co_efficient=st.sidebar.number_input("Reward Ratio Co-efficient",min_value=0.1,step=0.01)
  if st.sidebar.button("Evaluate"):
    coinData = st.session_state['DataFrame']
    coinData.index = pd.to_datetime(coinData.index)
    coinData = coinData[coinData.High != coinData.Low]
    coinData["VWAP"] = ta.vwap(coinData.High, coinData.Low, coinData.Close, coinData.Volume)
    coinData['RSI'] = ta.rsi(coinData.Close, length=rsiPeriod)
    my_bbands = ta.bbands(coinData.Close, length=bollPeriod, std=bollDev)
    coinData = coinData.join(my_bbands)
    st.write(coinData)
