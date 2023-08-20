from backtesting import Backtest, Strategy
from backtesting.test import GOOG
import streamlit as st
import talib
import time
import backtesting

class RSIOscillator(Strategy):
    upper_bound = 70
    lower_bound = 30
    rsi_timeperiod=14
    def init(self):
        self.rsi = self.I(talib.RSI, self.data.Close, self.rsi_timeperiod)
    
    def next(self):
        if self.rsi[-1] > self.params.upper_bound:
            self.position.close()
        elif self.rsi[-1] < self.params.lower_bound:
            self.buy()

def main():
    st.title("Backtesting Optimization Progress")
    bt=Backtest(GOOG,RSIOscillator,cash=10_000)
    strategyStats=bt.optimize(
    upper_bound=range(50,85,5), # Optimize Upper bound from 50-85 in steps of 5
    lower_bound=range(10,50,5), # Optimize Lower bound from 10-50 in steps of 5
    rsi_timeperiod=range(10,30,2) # Optimize the strategy with RSI timeperiod betweeen 10 and 30 in steps of 2
    )
    my_bar = st.progress(0)
    for percent_complete in range(Backtest.param_combos):
        #time.sleep(0.1)
        my_bar.progress(percent_complete + 1)
    st.write(strategyStats['_strategy'])

if __name__ == "__main__":
    main()
