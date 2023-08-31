from backtesting import Strategy
from backtesting import Backtest
from datetime import datetime
import numpy as np
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
class VWAPBOLLRSI:
    def __init__(self,previousCandles,bollPeriod,boll_dev,rsi_period,rsi_buyThreshold,rsi_sellThreshold,sl_coeff,tp_ratio):
        self.bollPeriod=bollPeriod
        self.boll_dev=boll_dev
        self.previousCandles=previousCandles
        self.rsi_period=rsi_period
        self.rsi_buyThreshold=rsi_buyThreshold
        self.rsi_sellThreshold=rsi_sellThreshold
        self.sl_coeff=sl_coeff
        self.tp_ratio=tp_ratio
        self.fig=None
        self.stat=None
    def implement(self,coinData):
        #coinData=pd.read_csv("DataTest.csv")
        coinData.index=pd.to_datetime(coinData.index)
        coinData=coinData[coinData.High!=coinData.Low] # Filter where there is no market movement.
        # len(coinData)
        # coinData.rename
        coinData["VWAP"]=ta.vwap(coinData.High, coinData.Low, coinData.Close, coinData.Volume)
        coinData['RSI']=ta.rsi(coinData.Close, length=self.rsi_period)
        my_bbands = ta.bbands(coinData.Close, length=self.bollPeriod, std=self.boll_dev)
        coinData=coinData.join(my_bbands)
        st.write(coinData)
        VWAPsignal = [0]*len(coinData)
        self.previousCandles = 15
        for thisRow in range(self.previousCandles, len(coinData)):
            upTrend = 1
            downTrend = 1
            for i in range(thisRow-self.previousCandles, thisRow+1):
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
            bbl_column_name = f'BBL_{self.bollPeriod}_{self.boll_dev}'
            bbu_column_name = f'BBU_{self.bollPeriod}_{self.boll_dev}'
            if (coinData.VWAPSignal[l]==2
                and coinData.Close[l]<=coinData[bbl_column_name][l]
                and coinData.RSI[l]<self.rsi_buyThreshold):
                    return 2
            if (coinData.VWAPSignal[l]==1
                and coinData.Close[l]>=coinData[bbu_column_name][l]
                and coinData.RSI[l]>self.rsi_sellThreshold):
                    return 1
            return 0

        TotSignal = [0]*len(coinData)
        for row in range(self.previousCandles, len(coinData)): #careful self.previousCandles used previous cell
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
        self.fig = go.Figure(data=[go.Candlestick(x=coinDatapl.index,
                        open=coinDatapl['Open'],
                        high=coinDatapl['High'],
                        low=coinDatapl['Low'],
                        close=coinDatapl['Close']),
                        go.Scatter(x=coinDatapl.index, y=coinDatapl.VWAP, 
                                   line=dict(color='blue', width=1), 
                                   name="VWAP"), 
                        go.Scatter(x=coinDatapl.index, y=coinDatapl['BBL_14_2.0'], 
                                   line=dict(color='green', width=1), 
                                   name="BBL"),
                        go.Scatter(x=coinDatapl.index, y=coinDatapl['BBU_14_2.0'], 
                                   line=dict(color='green', width=1), 
                                   name="BBU")])
        
        self.fig.add_scatter(x=coinDatapl.index, y=coinDatapl['pointposbreak'], mode="markers",
                        marker=dict(size=10, color="MediumPurple"),
                        name="Signal")
        #fig.show()
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
                slatr = self.sl_coeff*self.data.ATR[-1]
                TPSLRatio = self.tp_ratio
        
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
        self.stat = bt.run()
        #stat['Avg. Trade Duration']
        #bt.plot(show_legend=False)
        return self.fig,self.stat





