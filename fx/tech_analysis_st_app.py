import numpy as np
import streamlit as st
import sys
#from ta import trend
#sys.path.append('/app/business/fx')
sys.path.append('/app/business')
from technical_analysis import TIndicators
ta=TIndicators()
results=ta.MACD()
c=np.random.randn(100)
#macd=trend.MACD(close=c,window_slow=26,window_fast=12,window_sign=9)
st.write(results)
