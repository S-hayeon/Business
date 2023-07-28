import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
try:
  import sys
  #from ta import trend
  #sys.path.append('/app/business/fx')
  sys.path.append('/app/business')
except:
  import sys
  sys.path.append('/mount/src/business/')
from fx import main
from technical_analysis import TIndicators
#c=np.random.randn(100)
#macd=trend.MACD(close=c,window_slow=26,window_fast=12,window_sign=9)
if "CurrencyPair" not in st.session_state:
  st.session_state["CurrencyPair"]=""
currencypair=st.selectbox("Select you investment currency pair: ",main.maj_forex_pairs)
st.session_state["CurrencyPair"]=currencypair
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
