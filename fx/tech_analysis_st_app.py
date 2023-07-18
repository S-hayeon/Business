import sys
#from ta import trend
#sys.path.append('/app/business/fx')
sys.path.append('/app/business')
from fx import main
import numpy as np
import streamlit as st
from technical_analysis import TIndicators
ta=TIndicators()
results=ta.MACD()
c=np.random.randn(100)
#macd=trend.MACD(close=c,window_slow=26,window_fast=12,window_sign=9)
currencypair=st.selectbox("Select you investment currency pair: ",main.maj_forex_pairs)
#st.write(results)
data=main.collect_forex_data(f"{currencypair}{=X}")
st.write(data)
st.write(f"Yaani umechagua {currencypair}")
