from backtesting import Backtest, Strategy
from backtesting.test import GOOG
import streamlit as st
import talib
import time
import backtesting
from tradingpatterns.tradingpatterns import detect_head_shoulder

def main():
    st.title("Head shoulders")
    head_shoulder=detect_head_shoulder(df=st.session_state["DataFrame"])
    head_shoulder[['Date','head_shoulder_pattern']]
    st.write(head_shoulder)
    

if __name__ == "__main__":
    main()
