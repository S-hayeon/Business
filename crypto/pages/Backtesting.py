from backtesting import Backtest, Strategy
import matplotlib.pyplot as plt
import pandas as pd
import os
import streamlit as st
import talib
import time

st.title(f"Backtesting the {st.session_state['CurrencyPair']} Coin Pair")
selected_indicators = st.sidebar.multiselect("Select Technical Indicators", ['RSI', 'SMA', 'EMA', 'ADX'])
backtesting_strat_image = f"{st.session_state['CoinPair']}{selected_indicators}_strategy_results"
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
                self.should_buy = self.should_buy or (self.rsi_lower_bound<last_value) and (last_value<self.rsi_upper_bound)
                self.should_sell =self.should_sell or (last_value<self.rsi_lower_bound)
            elif indicator_name == 'EMA':
                self.should_buy =self.should_buy or (last_value>self.data.Close[-1])
                self.should_sell =self.should_sell or (last_value<self.data.Close[-1])
            elif indicator_name == 'SMA':
                self.should_buy =self.should_buy or (last_value>self.data.Close[-1])
                self.should_sell =self.should_sell or (last_value<self.data.Close[-1])
            elif indicator_name == 'ADX':
                if self.adx_upper_bound is None:
                    self.should_buy =self.should_buy or(last_value>self.adx_time_period)
                    self.should_sell =self.should_sell or (last_value>self.adx_time_period)
                elif self.adx_upper_bound is not None:
                    self.should_buy =self.should_buy or(last_value<self.adx_upper_bound) and (last_value>self.adx_lower_bound)
                    self.should_sell =self.should_sell or(last_value<self.adx_upper_bound) and (last_value>self.adx_lower_bound)
                else:
                    pass
        if self.should_sell:
            self.position.close()
        elif self.should_buy:
            self.buy()
###################################################### Sidebar inputs ##############################
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
        MyStrategy.rsi_lower_bound = st.sidebar.slider("Enter the RSI Lower Limit", 0, 100, step=1)
        MyStrategy.rsi_upper_bound = st.sidebar.slider("Enter the RSI Upper Limit", MyStrategy.rsi_lower_bound, 100, step=1)
        MyStrategy.rsi_time_period = st.sidebar.number_input("Enter the RSI Time Period", min_value=2, step=1)
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
    strategy_statsDF = pd.DataFrame(strategy_stats)
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')
    ax.table(cellText=strategy_statsDF.values, colLabels=strategy_statsDF.columns, cellLoc='center', loc='center')
    #ax.table(cellText=strategy_statsDF.values, colLabels=strategy_statsDF.columns,cellLoc='center')
    # Save the Matplotlib plot as an image
    plt.savefig(backtesting_strat_image,bbox_inches='tight', format='png')
    with st.container():
        # Display strategy statistics and equity curve
        stats_placeholder=st.empty()
        equity_placeholder=st.empty()
        equity_percent_placeholder=st.empty()
        with stats_placeholder.expander("Strategy Results"):
            #st.dataframe(pd.DataFrame(strategy_stats['_strategy']))
            # Create a Matplotlib plot from the DataFrame
            st.image(backtesting_strat_image, use_column_width=True)
            # if os.path.exists(backtesting_strat_image):
            #     os.remove(backtesting_strat_image)
            #st.dataframe(strategy_statsDF)
        with equity_placeholder.expander("Equity curve"):
            st.write("Equity Curve:")
            st.line_chart(strategy_stats['_equity_curve']['Equity'])
        with equity_percent_placeholder.expander("Equity Drawdown curve"):
            st.write("Equity Percentage Curve:")
            st.line_chart(strategy_stats['_equity_curve']['DrawdownPct'])
