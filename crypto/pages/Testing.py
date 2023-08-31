import pandas as pd
import pandas_ta as ta
import streamlit as st
coinData = st.session_state['DataFrame']
coinData.index = pd.to_datetime(coinData.index)
coinData = coinData[coinData.High != coinData.Low]
coinData["VWAP"] = ta.vwap(coinData.High, coinData.Low, coinData.Close, coinData.Volume)
coinData['RSI'] = ta.rsi(coinData.Close, length=16)
my_bbands = ta.bbands(coinData.Close, length=14, std=2.0)
coinData = coinData.join(my_bbands)
st.write(coinData)
