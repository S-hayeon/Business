from backtesting import Strategy
from backtesting import Backtest
from datetime import datetime
import numpy as np
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
strategies=['VWAP_Bollinger_RSI','None']
strategy=st.selectbox("My preferred Strategy is",strategies)
if strategy=='VWAP_Bollinger_RSI':
  mode=st.sidebar.radio("Enter Mode",options=['Manual','Automatic'])
  if mode=='Manual':
    previousCandles=st.sidebar.number_input("No of Previous candles",min_value=3,step=1)
    bollPeriod=st.sidebar.number_input("Bollinger Bands Time period",min_value=2,step=1)
    bollDev=st.sidebar.number_input("Bollinger Bands Standard Deviation",min_value=1,step=1)
    rsiPeriod=st.sidebar.number_input("RSI Time period",min_value=2,step=1)
    rsi_buyThreshold=st.sidebar.number_input("RSI Buy Threshold",min_value=5,step=1)
    rsi_sellThreshold=st.sidebar.number_input("RSI Sell Threshold",min_value=rsi_buyThreshold,step=1)
    sl_co_efficient=st.sidebar.number_input("Stop Loss Co-efficient",min_value=0.1,step=0.01)
    tp_co_efficient=st.sidebar.number_input("Reward Ratio Co-efficient",min_value=0.1,step=0.01)
    if st.sidebar.button("Evaluate"):
      coinData = st.session_state['DataFrame']
      # # Loop to remove columns containing "BB" in their names
      # columns_to_remove = []
      # for column in coinData.columns:
      #   if 'BB' in column:
      #     columns_to_remove.append(column)
      #coinData.drop(columns=columns_to_remove, inplace=True) # Now the DataFrame coinData will no longer have columns containing "BB" in their names
      coinData.index = pd.to_datetime(coinData.index)
      coinData = coinData[coinData.High != coinData.Low]
      coinData["VWAP"] = ta.vwap(coinData.High, coinData.Low, coinData.Close, coinData.Volume)
      coinData['RSI'] = ta.rsi(coinData.Close, length=rsiPeriod)
      my_bbands = ta.bbands(coinData.Close, length=bollPeriod, std=bollDev)
      bbl_column_name = f'BBL_{bollPeriod}_{float(bollDev)}'
      bbu_column_name = f'BBU_{bollPeriod}_{float(bollDev)}'
      coinData = coinData.join(my_bbands)
      st.write(f'BBU Upper is referred to: {bbu_column_name}')
      st.write(f'Columns: {coinData.columns}')
      st.write(f'BBU Column: {bbu_column_name in coinData.columns}')
      VWAPsignal = [0]*len(coinData)
      for thisRow in range(previousCandles, len(coinData)):
        upTrend = 1
        downTrend = 1
        for i in range(thisRow-previousCandles, thisRow+1):
          if max(coinData.Open[i], coinData.Close[i])>=coinData.VWAP[i]:
              downTrend=0
          if min(coinData.Open[i], coinData.Close[i])<=coinData.VWAP[i]:
              upTrend=0
      if upTrend==1 and downTrend==1:
          VWAPsignal[thisRow]=3
      elif upTrend==1:
          VWAPsignal[thisRow]=2
      elif downTrend==1:
          VWAPsignal[thisRow]=1
      coinData['VWAPSignal'] = VWAPsignal
      def Entry_Exit_Signal(l):
          if (coinData.VWAPSignal[l]==2
              #and coinData.Close[l]<=coinData['BBL_14_2.0'][l]
              and coinData.Close[l]<=coinData[bbl_column_name][l]
              and coinData.RSI[l]<45):
                  return 2
          if (coinData.VWAPSignal[l]==1
              #and coinData.Close[l]>=coinData['BBU_14_2.0'][l]
              and coinData.Close[l]>=coinData[bbu_column_name][l]
              and coinData.RSI[l]>55):
                  return 1
          return 0
      TotSignal = [0]*len(coinData)
      for row in range(previousCandles, len(coinData)): #careful previousCandles used previous cell
          TotSignal[row] = Entry_Exit_Signal(row)
      coinData['Entry_Exit_Signal'] = TotSignal
      coinData[coinData.Entry_Exit_Signal!=0].count()
      def pointposbreak(x):
          if x['Entry_Exit_Signal']==1:
              return x['High']+1e-4
          elif x['Entry_Exit_Signal']==2:
              return x['Low']-1e-4
          else:
              return np.nan
      coinData['pointposbreak'] = coinData.apply(lambda row: pointposbreak(row), axis=1)
      st_var=10400
      coinDatapl = coinData[st_var:st_var+350]
      coinDatapl.reset_index(inplace=True)
      fig = go.Figure(data=[go.Candlestick(x=coinDatapl.index,
                      open=coinDatapl['Open'],
                      high=coinDatapl['High'],
                      low=coinDatapl['Low'],
                      close=coinDatapl['Close']),
                      go.Scatter(x=coinDatapl.index, y=coinDatapl.VWAP, 
                                 line=dict(color='blue', width=1), 
                                 name="VWAP"), 
                      go.Scatter(x=coinDatapl.index, y=coinDatapl[bbl_column_name], 
                                 line=dict(color='green', width=1), 
                                 name="BBL"),
                      go.Scatter(x=coinDatapl.index, y=coinDatapl[bbu_column_name], 
                                 line=dict(color='green', width=1), 
                                 name="BBU")])
      
      fig.add_scatter(x=coinDatapl.index, y=coinDatapl['pointposbreak'], mode="markers",
                      marker=dict(size=10, color="MediumPurple"),
                      name="Signal")
      fig.show()
      coinDatapl = coinData[:75000].copy()
      coinDatapl['ATR']=ta.atr(coinDatapl.High, coinDatapl.Low, coinDatapl.Close, length=7)
      #help(ta.atr)
      def SIGNAL():
          return coinDatapl.Entry_Exit_Signal
      
      class MyVWAP_Boll_RSI_Strategy(Strategy):
          initsize = 0.99
          mysize = initsize
          def init(self):
              super().init()
              self.signal1 = self.I(SIGNAL)
      
          def next(self):
              super().next()
              #slatr = 1.2*self.data.ATR[-1]
              slatr = sl_co_efficient*self.data.ATR[-1]
              TPSLRatio = tp_co_efficient
      
              if len(self.trades)>0:
                  if self.trades[-1].is_long and self.data.RSI[-1]>=90:
                      self.trades[-1].close()
                  elif self.trades[-1].is_short and self.data.RSI[-1]<=10:
                      self.trades[-1].close()
              if self.signal1==2 and len(self.trades)==0:
                  sl1 = self.data.Close[-1] - slatr
                  tp1 = self.data.Close[-1] + slatr*TPSLRatio
                  self.buy(sl=sl1, tp=tp1, size=self.mysize)
              elif self.signal1==1 and len(self.trades)==0:
                  sl1 = self.data.Close[-1] + slatr
                  tp1 = self.data.Close[-1] - slatr*TPSLRatio
                  self.sell(sl=sl1, tp=tp1, size=self.mysize)
      
      bt = Backtest(coinDatapl, MyVWAP_Boll_RSI_Strategy, cash=100, margin=1/10, commission=0.00)
      stat = bt.run()
      import streamlit as st
      with st.container():
        with st.expander("Strategy Buy and Sell Points"):
          #st.pyplot(bt.plot())
          st.write("In Development")
        with st.expander("Strategy Performance"):
          st.dataframe(stat)
        with st.expander("Equity curve"):
          st.line_chart(stat['_equity_curve'])
        with st.expander("Average Trade duration"):
          st.write(stat['Avg. Trade Duration'])
        with st.expander("Equity Drawdown curve"):
          st.line_chart(stat['_equity_curve']['DrawdownPct'])
        with st.expander("Equity curve"):
          st.line_chart(stat['_equity_curve'])
  else:
    class MyVWAP_Boll_RSI_Strategy(Strategy):
        previousCandles=15
        bollPeriod=14
        bollDev=2
        rsiPeriod=14
        rsi_buyThreshold=35
        rsi_sellThreshold=55
        sl_co_efficient=0.5
        tp_co_efficient=1.2
        data = st.session_state['DataFrame']
        def init(self):
            super().init()
            self.data.index = pd.to_datetime(self.data.index)
            self.data = self.data[self.data.High != self.data.Low]
            self.data["VWAP"] = ta.vwap(self.data.High, self.data.Low, self.data.Close, self.data.Volume)
            self.data['RSI'] = ta.rsi(self.data.Close, length=self.rsiPeriod)
            my_bbands = ta.bbands(self.data.Close, length=self.bollPeriod, std=self.bollDev)
            bbl_column_name = f'BBL_{self.bollPeriod}_{float(self.bollDev)}'
            bbu_column_name = f'BBU_{self.bollPeriod}_{float(self.bollDev)}'
            self.data = self.data.join(my_bbands)
            # #print(f'BBU Upper is referred to: {bbu_column_name}')
            # print(f'Columns: {self.data.columns}')
            # print(f'BBU Column: {bbu_column_name in self.data.columns}')
            VWAPsignal = [0]*len(self.data)
            for thisRow in range(self.previousCandles, len(self.data)):
              upTrend = 1
              downTrend = 1
              for i in range(thisRow-self.previousCandles, thisRow+1):
                if max(self.data.Open[i], self.data.Close[i])>=self.data.VWAP[i]:
                    downTrend=0
                if min(self.data.Open[i], self.data.Close[i])<=self.data.VWAP[i]:
                    upTrend=0
            if upTrend==1 and downTrend==1:
                VWAPsignal[thisRow]=3
            elif upTrend==1:
                VWAPsignal[thisRow]=2
            elif downTrend==1:
                VWAPsignal[thisRow]=1
            self.data['VWAPSignal'] = VWAPsignal
            def Entry_Exit_Signal(l):
                if (self.data.VWAPSignal[l]==2
                    #and self.data.Close[l]<=self.data['BBL_14_2.0'][l]
                    and self.data.Close[l]<=self.data[bbl_column_name][l]
                    and self.data.RSI[l]<self.rsi_buyThreshold):
                        return 2
                if (self.data.VWAPSignal[l]==1
                    #and self.data.Close[l]>=self.data['BBU_14_2.0'][l]
                    and self.data.Close[l]>=self.data[bbu_column_name][l]
                    and self.data.RSI[l]>self.rsi_sellThreshold):
                        return 1
                return 0
            TotSignal = [0]*len(self.data)
            for row in range(self.previousCandles, len(self.data)): #careful self.previousCandles used previous cell
                TotSignal[row] = Entry_Exit_Signal(row)
            self.data['Entry_Exit_Signal'] = TotSignal
            st=10400
            coinDatapl = self.data[st:st+350]
            coinDatapl.reset_index(inplace=True)
            coinDatapl = self.data[:75000].copy()
            self.data['ATR']=ta.atr(self.data.High, self.data.Low, self.data.Close, length=7)
            def SIGNAL():
                #return coinDatapl.Entry_Exit_Signal
                return self.data['Entry_Exit_Signal']
            self.signal1 = self.I(SIGNAL)
        def next(self):
            super().next()
            #slatr = 1.2*self.data.ATR[-1]
            slatr = self.sl_co_efficient*self.data.ATR[-1]
            TPSLRatio = self.tp_co_efficient
    
            if len(self.trades)>0:
                if self.trades[-1].is_long and self.data.RSI[-1]>=90:
                    self.trades[-1].close()
                elif self.trades[-1].is_short and self.data.RSI[-1]<=10:
                    self.trades[-1].close()
            if self.signal1==2 and len(self.trades)==0:
                sl1 = self.data.Close[-1] - slatr
                tp1 = self.data.Close[-1] + slatr*TPSLRatio
                self.buy(sl=sl1, tp=tp1, size=self.mysize)
            elif self.signal1==1 and len(self.trades)==0:
                sl1 = self.data.Close[-1] + slatr
                tp1 = self.data.Close[-1] - slatr*TPSLRatio
                self.sell(sl=sl1, tp=tp1, size=self.mysize)
    bt = Backtest(st.session_state['DataFrame'], MyVWAP_Boll_RSI_Strategy, cash=100, margin=1/10, commission=0.00)
    #stats=bt.optimize(previousCandles=range(2,30,1),bollPeriod=range(2,30,1),bollDev=range(1,5,1),rsiPeriod=range(2,30,1),rsi_buyThreshold=range(5,50,1),rsi_sellThreshold=range(51,80,1))
    vwapBoll_params = {
    'Candles': {'previousCandles': range(2, 30, 1)},
    'Bollinger': {'bollPeriod': range(2, 30, 1), 'bollDev': range(1, 5, 1)},
    'Profit':{'Profit Factor'},
    'RSI': {
        'rsiPeriod': range(2, 30, 1),
        'rsi_buyThreshold': range(5, 50, 1),
        'rsi_sellThreshold': range(51, 80, 1)
    }
}
    metrics_dict = {
    "Profit": "Profit Factor",
    "WinRate": "Win Rate [%]",
    "Expectancy": "Expectancy [%]",
    "Calmar": "Calmar Ratio",
    "Sharpe": "Sharpe Ratio",
    "Sortino": "Sortino Ratio"
}
    optimizationMode=st.radio("Your preferred optimization",options=['Indicators','Metrics'])
    if optimizationMode=='Indicators':
      selected_key = st.selectbox("Select Parameter:", list(vwapBoll_params.keys())) # Create a Streamlit selectbox to choose the key
      if st.button("Find optimized values"):
        #stats = {} # Initialize stats with an empty dictionary
        stats = None
        param_dict = vwapBoll_params[selected_key] # Extract the parameter settings dictionary
        param_string = ', '.join(f"{key}=range({value.start}, {value.stop}, {value.step})" for key, value in param_dict.items())
        stats = bt.optimize(**eval(f"dict({param_string})")) # Evaluate the param_string and pass it as keyword arguments using eval()
    if optimizationMode=='Metrics':
      selected_metric = st.selectbox("Select a metric:", list(metrics_dict.keys()))
      metric_format = metrics_dict.get(selected_metric)
      if metric_format is not None:
        stats = bt.optimize(rsi_sellThreshold=range(20,100,1),maximize=metric_format)
      with st.container():
        with st.expander("Strategy KPI Performance"):
          #st.dataframe(stats[selected_key])
          st.dataframe(stats)
        with st.expander(f'Optimal Values for {selected_key} in Strategy'):
          st.write(stats['_strategy'])
        
