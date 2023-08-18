from backtesting import Backtest, Strategy
import streamlit as st
import talib
import pandas as pd
import time

selected_indicators = st.multiselect("Select Technical Indicators", ['RSI', 'SMA', 'EMA', 'ADX'])

class MyStrategy(Strategy):
    
    def init(self):
        self.indicators = {}
        self.should_buy=False
        self.should_sell=False
        if 'RSI' in selected_indicators:
            self.indicators['RSI'] = self.I(talib.RSI, self.data.Close, self.time_period)
        if 'SMA' in selected_indicators:
            self.indicators['SMA'] = self.I(talib.SMA, self.data.Close, timeperiod=self.time_period)
        if 'EMA' in selected_indicators:
            self.indicators['EMA'] = self.I(talib.EMA, self.data.Close, timeperiod=self.time_period)
        if 'ADX' in selected_indicators:
            self.indicators['ADX'] = self.I(talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=self.time_period)

    def next(self):
        for indicator_name, indicator_values in self.indicators.items():
            last_value = indicator_values[-1]
            if indicator_name == 'RSI':
                self.should_buy = self.should_buy and (self.lower_bound<self.last_value<self.upper_bound)
                self.should_sell =self.should_sell and (last_value<self.lower_bound)
            elif indicator_name == 'EMA':
                self.should_buy =self.should_buy and (last_value>self.data.Close[-1])
                self.should_sell =self.should_sell and (last_value<self.data.Close[-1])
            elif indicator_name == 'ADX':
                self.should_buy =self.should_buy and(last_value>self.time_period)
                self.should_sell =self.should_sell and (last_value>self.time_period)
        if self.should_sell:
            self.position.close()
        elif self.should_buy:
            self.buy()

# Streamlit app
st.title(f"Backtesting the {st.session_state['CurrencyPair']} Coin Pair")

###################################################### Sidebar inputs ##############################
if 'ADX' in selected_indicators:
    MyStrategy.upper_bound = None
    MyStrategy.lower_bound = None
    MyStrategy.time_period = st.sidebar.number_input("Enter the ADX Indicator Time Period",min_value=1,step=1)
    st.toast("Strategy buys and sells when the last close is above the ADX")
    time.sleep(2)
elif 'EMA' in selected_indicators:
    MyStrategy.upper_bound = None
    MyStrategy.lower_bound = None
    MyStrategy.time_period = st.sidebar.number_input("Enter the EMAIndicator Time Period", min_value=1,step=1)
    st.toast("Strategy buys when the last close is above the EMA")
    time.sleep(2)
elif 'RSI' in selected_indicators:
    MyStrategy.upper_bound=st.sidebar.slider("Enter the RSI Upper Limit",0,100,step=1)
    MyStrategy.lower_bound=st.sidebar.slider("Enter the RSI Lower Limit",0,100,step=1)
    MyStrategy.time_period = st.sidebar.number_input("Enter the RSI Time Period", min_value=1,step=1)
    time.sleep(2)
elif 'SMA' in selected_indicators:
    MyStrategy.upper_bound = None
    MyStrategy.lower_bound = None
    MyStrategy.time_period = st.sidebar.number_input("Enter the SMA Indicator Time Period",min_value=1,step=1)
    st.toast("Strategy buys when the last close is above the SMA")
    time.sleep(2)
else:
    pass

data = st.session_state['DataFrame']

# Run backtest on button click
if st.sidebar.button("Test my strategy"):
    bt = Backtest(data, MyStrategy, cash=10000)
    strategy_stats = bt.run()

    with st.container():
        # Display strategy statistics and equity curve
        stats_placeholder=st.empty()
        equity_placeholder=st.empty()
        equity_percent_placeholder=st.empty()
        with stats_placeholder.expander("Strategy Results"):
            #st.dataframe(pd.DataFrame(strategy_stats['_strategy']))
            st.dataframe(pd.DataFrame(strategy_stats))
        with equity_placeholder.expander("Equity Drawdown curve"):
            st.write("Equity Curve:")
            st.line_chart(strategy_stats['_equity_curve']['Equity'])
        with equity_percent_placeholder.expander("Equity Drawdown curve"):
            st.write("Equity Percentage Curve:")
            st.line_chart(strategy_stats['_equity_curve']['DrawdownPct'])
