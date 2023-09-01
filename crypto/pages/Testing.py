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
    st=10400
    coinDatapl = coinData[st:st+350]
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
            slatr = 1.2*self.data.ATR[-1]
            TPSLRatio = 1.5
    
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
    stat['Avg. Trade Duration']
    #bt.plot(show_legend=False)
