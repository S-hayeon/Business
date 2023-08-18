from backtesting import Backtest,Strategy
from backtesting.lib import crossover,plot_heatmaps
import pandas as pd
import streamlit as st
import talib
class MyStrategy(Strategy):
  upper_bound=st.sidebar.slider("Enter the Indicator Upper Limit",0, 100)
  lower_bound=st.sidebar.slider("Enter the Indicator Lower Limit",0, 100)
  def init(self):
    self.indicator1=self.I(talib.RSI,self.data.Close,self.time_period)
  def next(self):
    if self.indicator[-1]>self.upper_bound:
      self.position.close()
    elif self.indicator[-1]<self.lower_bound:
      self.buy()
cash=st.sidebar.slider("Enter you available cash",0,10000,step=10)
if st.sidebar.button("Test my strategy"):
  if st.session_state["DataFrame"] is not None:
    bt=Backtest(st.session_state["DataFrame"],MyStrategy,cash)
    strategyStats=bt.run()
    strategyStatsDF=pd.DataFrame(strategyStats)
    strategyTradesDF=pd.DataFrame(strategyStats['_trades'])
    with st.container():
      strategyStats_placeholder=st.empty()
      strategyTrades_placeholder=st.empty()
      with strategyStats_placeholder.expander("View Stategy Statistics"):
        st.dataframe(strategyStatsDF)
      with strategyTrades_placeholder.expander("View Strategy Trades"):
        st.dataframe(strategyTradesDF)
      
      
