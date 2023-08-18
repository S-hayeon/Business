from backtesting import Backtest,Strategy
from backtesting.lib import crossover,plot_heatmaps
import pandas as pd
import streamlit as st
import talib
selected_indicators = st.multiselect("Select Technical Indicators", ['RSI', 'SMA', 'EMA', 'ADX']
class MyStrategy(Strategy):
  def init(self):
    self.indicators = {}
    if 'RSI' in selected_indicators:
      self.indicators['RSI'] = self.I(talib.RSI, self.data.Close, time_period)
    if 'SMA' in selected_indicators:
      self.indicators['SMA'] = self.I(talib.SMA, self.data.Close, timeperiod=time_period)
    if 'EMA' in selected_indicators:
      self.indicators['EMA'] = self.I(talib.EMA, self.data.Close, timeperiod=time_period)
    if 'ADX' in selected_indicators:
      self.indicators['ADX'] = self.I(talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=time_period)

    def next(self):
      for indicator_name, indicator_values in self.indicators.items():
        last_value = indicator_values[-1]
        if indicator_name == 'RSI':
          if last_value > upper_bound:
            self.position.close()
          elif last_value < lower_bound:
            self.buy()
        elif indicator_name == 'EMA' or indicator_name == 'ADX':
          if last_value > upper_bound:
            self.position.close()
          elif last_value < lower_bound:
               self.buy()
#cash=st.sidebar.slider("Enter you available cash",0,10000,step=10)
if st.sidebar.button("Test my strategy"):
  if st.session_state["DataFrame"] is not None:
    bt=Backtest(st.session_state["DataFrame"],MyStrategy,cash=10000)
    strategyStats=bt.run()
    strategyStatsDF=pd.DataFrame(strategyStats)
    #strategyTradesDF=pd.DataFrame(strategyStats['_trades'])
    with st.container():
      strategyStats_placeholder=st.empty()
      strategyTrades_placeholder=st.empty()
      with strategyStats_placeholder.expander("View Stategy Statistics"):
        st.dataframe(strategyStatsDF)
      with strategyTrades_placeholder.expander("View Strategy Trades"):
        #st.dataframe(strategyTradesDF)
        st.write(strategyStats['_equity_curve'])
      
      
