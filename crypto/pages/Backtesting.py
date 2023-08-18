from backtesting import Backtest, Strategy
import streamlit as st
import talib
import pandas as pd

selected_indicators = st.multiselect("Select Technical Indicators", ['RSI', 'SMA', 'EMA', 'ADX'])

class MyStrategy(Strategy):
    def init(self):
        self.indicators = {}
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
                if last_value > self.upper_bound:
                    self.position.close()
                elif last_value < self.lower_bound:
                    self.buy()
            elif indicator_name == 'EMA' or indicator_name == 'ADX':
                if last_value > self.upper_bound:
                    self.position.close()
                elif last_value < self.lower_bound:
                    self.buy()

# Streamlit app
st.title("Backtesting")

# Sidebar inputs
MyStrategy.upper_bound = st.sidebar.slider("Enter the Indicator Upper Limit", 0, 100)
MyStrategy.lower_bound = st.sidebar.slider("Enter the Indicator Lower Limit", 0, 100)
MyStrategy.time_period = st.sidebar.slider("Enter the Indicator Time Period", 0, 30)

data = st.session_state['DataFrame']

# Run backtest on button click
if st.sidebar.button("Test my strategy"):
    bt = Backtest(data, MyStrategy, cash=10000)
    strategy_stats = bt.run()

    with st.container():
        # Display strategy statistics and equity curve
        st.write("Strategy Statistics:")
        st.dataframe(pd.DataFrame(strategy_stats['_strategy']))
        
        st.write("Equity Curve:")
        st.line_chart(strategy_stats['_equity_curve'])
