from backtesting import Backtest, Strategy
import streamlit as st
import talib
import pandas as pd
import time

st.title(f"Backtesting the {st.session_state['CurrencyPair']} Coin Pair")
selected_indicators = st.multiselect("Select Technical Indicators", ['RSI', 'SMA', 'EMA', 'ADX'])
class MyStrategy(Strategy):
    def init(self):
        self.indicators = {}
        self.should_buy=False
        self.should_sell=False
        if 'RSI' in selected_indicators:
            self.indicators['RSI'] = self.I(talib.RSI, self.data.Close, self.rsi_time_period)
        if 'SMA' in selected_indicators:
            self.indicators['SMA'] = self.I(talib.SMA, self.data.Close, timeperiod=self.sma_time_period)
        if 'EMA' in selected_indicators:
            self.indicators['EMA'] = self.I(talib.EMA, self.data.Close, timeperiod=self.ema_time_period)
        if 'ADX' in selected_indicators:
            self.indicators['ADX'] = self.I(talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=self.adx_time_period)

    def next(self):
        for indicator_name, indicator_values in self.indicators.items():
            last_value = indicator_values[-1]
            if indicator_name == 'RSI':
                self.should_buy = self.should_buy and (self.rsi_lower_bound<self.last_value<self.rsi_upper_bound)
                self.should_sell =self.should_sell and (last_value<self.rsi_lower_bound)
            elif indicator_name == 'EMA':
                self.should_buy =self.should_buy and (last_value>self.data.Close[-1])
                self.should_sell =self.should_sell and (last_value<self.data.Close[-1])
            elif indicator_name == 'SMA':
                self.should_buy =self.should_buy and (last_value>self.data.Close[-1])
                self.should_sell =self.should_sell and (last_value<self.data.Close[-1])
            elif indicator_name == 'ADX':
                if self.adx_upper_bound is None:
                    self.should_buy =self.should_buy and(last_value>self.adx_time_period)
                    self.should_sell =self.should_sell and (last_value>self.adx_time_period)
                elif self.adx_upper_bound is not None:
                    self.should_buy =self.should_buy and(last_value<self.adx_upper_bound) and (last_value>self.adx_lower_bound)
                    self.should_sell =self.should_sell and(last_value<self.adx_upper_bound) and (last_value>self.adx_lower_bound)
                else:
                    pass
        if self.should_sell:
            self.position.close()
        elif self.should_buy:
            self.buy()


###################################################### Sidebar inputs ##############################
mode=st.radio("Do you have the indicators' values?"['Yes','No'])
if mode=='Yes':
    # Separate the indicator-specific sidebar inputs into their own blocks
    for indicator_name in selected_indicators:
        if indicator_name == 'ADX':
            range_value_choice=st.sidebar.selectbox("Do you want one ADX value or range?",['One Value','Range'])
            if range_value_choice=='One Value':
                MyStrategy.adx_upper_bound=None
                MyStrategy.adx_lower_bound = st.sidebar.slider("ADX Value, Buy/Sell when ADX is or above:", 0, 40, step=1)
                MyStrategy.adx_time_period = st.sidebar.number_input("ADX Indicator Time Period", min_value=1, step=1)
                st.toast("Knowledge Nugget: ADX shows a trending market",icon="💹")
            elif range_value_choice=='Range':
                MyStrategy.adx_upper_bound = st.sidebar.slider("ADX Value, Buy/Sell when ADX is or below:", 0, 40, step=1)
                MyStrategy.adx_lower_bound = st.sidebar.slider("ADX Value, Buy/Sell when ADX is or above:", 0, 40, step=1)
                MyStrategy.adx_time_period = st.sidebar.number_input("Enter the ADX Indicator Time Period", min_value=1, step=1)
                if MyStrategy.adx_upper_bound>MyStrategy.adx_lower_bound:
                    st.toast("Knowledge Nugget: ADX shows a trending market",icon="💹")
                else:
                    st.toast("The ADX Upper limit should be higher the ADX Lower limit",icon="⚠️")
            time.sleep(2)
        elif indicator_name == 'EMA':
            MyStrategy.ema_upper_bound = None
            MyStrategy.ema_lower_bound = None
            MyStrategy.ema_time_period = st.sidebar.number_input("Enter the EMA Indicator Time Period", min_value=1, step=1)
            st.toast("Strategy buys when the last close is above the EMA")
            time.sleep(2)
        elif indicator_name == 'RSI':
            MyStrategy.rsi_upper_bound = st.sidebar.slider("Enter the RSI Upper Limit", 0, 100, step=1)
            MyStrategy.rsi_lower_bound = st.sidebar.slider("Enter the RSI Lower Limit", 0, 100, step=1)
            MyStrategy.rsi_time_period = st.sidebar.number_input("Enter the RSI Time Period", min_value=1, step=1)
            time.sleep(2)
        elif indicator_name == 'SMA':
            MyStrategy.sma_upper_bound = None
            MyStrategy.sma_lower_bound = None
            MyStrategy.sma_time_period = st.sidebar.number_input("Enter the SMA Indicator Time Period", min_value=1, step=1)
            st.toast("Strategy buys when the last close is above the SMA")
            time.sleep(2)
    
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
            with equity_placeholder.expander("Equity curve"):
                st.write("Equity Curve:")
                st.line_chart(strategy_stats['_equity_curve']['Equity'])
            with equity_percent_placeholder.expander("Equity Drawdown curve"):
                st.write("Equity Percentage Curve:")
                st.line_chart(strategy_stats['_equity_curve']['DrawdownPct'])
if mode=='No':
    # Separate the indicator-specific sidebar inputs into their own blocks
    for indicator_name in selected_indicators:
        if indicator_name == 'ADX':
            MyStrategy.adx_upper_bound = st.sidebar.number_input("ADX Value Upper Limit:", min_value=10, step=1)
            MyStrategy.adx_lower_bound = st.sidebar.number_input("ADX Value Lower Limit:", min_value=0, step=1)
            MyStrategy.adx_time_period_upper = st.sidebar.number_input("Enter the ADX Indicator Time Period Upper", min_value=1, step=1)
            MyStrategy.adx_time_period_lower = st.sidebar.number_input("Enter the ADX Indicator Time Period Lower", min_value=1, step=1)
            if MyStrategy.adx_upper_bound > MyStrategy.adx_lower_bound:
                st.toast("Knowledge Nugget: ADX shows a trending market", icon="💹")
            else:
                st.toast("The ADX Upper limit should be higher than the ADX Lower limit", icon="⚠️")
            time.sleep(2)
        elif indicator_name == 'EMA':
            MyStrategy.ema_upper_bound = st.sidebar.number_input("EMA Indicator Time Period Upper Limit", min_value=1, step=1)
            MyStrategy.ema_lower_bound = st.sidebar.number_input("EMA Indicator Time Period Lower Limit", min_value=1, step=1)
            MyStrategy.ema_time_period = None
            st.toast("Strategy buys when the last close is above the EMA")
            time.sleep(2)
        elif indicator_name == 'RSI':
            MyStrategy.rsi_upper_bound = st.sidebar.slider("Enter the RSI Upper Limit", 0, 100, step=1)
            MyStrategy.rsi_lower_bound = st.sidebar.slider("Enter the RSI Lower Limit", 0, 100, step=1)
            MyStrategy.rsi_time_period_upper = st.sidebar.number_input("Enter the RSI Time Period Upper Limit", min_value=1, step=1)
            MyStrategy.rsi_time_period_lower = st.sidebar.number_input("Enter the RSI Time Period Lower Limit", min_value=1, step=1)
            time.sleep(2)
        elif indicator_name == 'SMA':
            MyStrategy.sma_upper_bound = st.sidebar.number_input("SMA Indicator Time Period Upper Limit", min_value=1, step=1)
            MyStrategy.sma_lower_bound = st.sidebar.number_input("SMA Indicator Time Period Lower Limit", min_value=1, step=1)
            MyStrategy.sma_time_period = None
            st.toast("Strategy buys when the last close is above the SMA")
            time.sleep(2)
        else:
            pass
    
    # Load data
    data = st.session_state['DataFrame']
    
    # Create a dictionary to hold indicator-specific optimization ranges
    indicator_ranges = {
        'ADX': {
            'upper_bound': range(5, MyStrategy.adx_upper_bound, 5),
            'lower_bound': range(MyStrategy.adx_lower_bound, 50, 5),
            'adx_timeperiod': range(MyStrategy.adx_time_period_lower, MyStrategy.adx_time_period_upper, 2)
        },
        'EMA': {
            'ema_10_timeperiod': range(MyStrategy.ema_lower_bound, MyStrategy.ema_upper_bound, 10)
        },
        'RSI': {
            'upper_bound': range(30, MyStrategy.rsi_upper_bound, 5),
            'lower_bound': range(1,MyStrategy.rsi_lower_bound, 5),
            'rsi_timeperiod': range(MyStrategy.rsi_time_period_lower, MyStrategy.rsi_time_period_upper, 2)
        },
        'SMA': {
            'sma_time_period': range(MyStrategy.sma_lower_bound, MyStrategy.sma_upper_bound, 2)
        }
    }
    # Create a dictionary to hold indicator-specific parameters
    indicator_params = {}
    
    # Populate indicator_params based on selected indicators
    for indicator_name in selected_indicators:
        indicator_params.update(indicator_ranges.get(indicator_name, {}))
    # Run backtest on button click
    if st.sidebar.button("Test my strategy"):
        bt = Backtest(data, MyStrategy, cash=10000)
        strategyStats = bt.optimize(**indicator_params)
        #strategy_stats = bt.run()
        with st.container():
            # Display strategy statistics and equity curve
            stats_placeholder=st.empty()
            equity_placeholder=st.empty()
            equity_percent_placeholder=st.empty()
            with stats_placeholder.expander("Strategy"):
                st.write(strategyStats['_strategy'])
            with equity_placeholder.expander("Equity curve"):
                st.write("Equity Curve:")
                st.line_chart(strategy_stats['_equity_curve']['Equity'])
            with equity_percent_placeholder.expander("Equity Drawdown curve"):
                st.write("Equity Percentage Curve:")
                st.line_chart(strategy_stats['_equity_curve']['DrawdownPct'])
