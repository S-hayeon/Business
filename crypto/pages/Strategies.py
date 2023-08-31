import streamlit as st
from TradingStrategies import vwap_BollRsiScalping
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
  #prevCandles=15
  # bollPeriod=14
  # bollDev=2
  # rsiPeriod=16
  # rsi_buyThreshold=45
  # rsi_sellThreshold=55
  # sl_co_efficient=1.2
  # tp_co_efficient=1.5
  if st.sidebar.button("Evaluate"):
    vwapBoll=vwap_BollRsiScalping.VWAPBOLLRSI(prevCandles,bollPeriod,bollDev,rsiPeriod,rsi_buyThreshold,rsi_sellThreshold,sl_co_efficient,tp_co_efficient)
    data=st.session_state['DataFrame']
    #st.write(data)
    vwapBollFigure,vwapll_stat=vwapBoll.implement(data)
    st.toast("Evaluating the VWAP Bollinger RSI strategy")
    with st.container():
      with st.expander("Strategy Buy and Sell Points"):
        st.pyplot(vwapBollFigure)
      with st.expander("Strategy Performance"):
        st.dataframe(vwapBoll_stat)
                                                  
  
