from backtesting import Backtest, Strategy
from backtesting.test import GOOG
import streamlit as st
import talib
import time
import backtesting

class RSIOscillator(Strategy):
    def __init__(self, upper_bound, lower_bound, rsi_timeperiod):
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound
        self.rsi_timeperiod = rsi_timeperiod
    
    def init(self):
        self.rsi = self.I(talib.RSI, self.data.Close, self.rsi_timeperiod)
    
    def next(self):
        if self.rsi[-1] > self.upper_bound:
            self.position.close()
        elif self.rsi[-1] < self.lower_bound:
            self.buy()

def optimize_strategy(upper_bound, lower_bound, rsi_timeperiod):
    bt = Backtest(GOOG, RSIOscillator, cash=10_000, upper_bound=upper_bound, lower_bound=lower_bound, rsi_timeperiod=rsi_timeperiod)
    strategy_stats = bt.run()
    return strategy_stats

def main():
    st.title("Backtesting Optimization Progress")

    upper_bounds = range(50, 85, 5)
    lower_bounds = range(10, 50, 5)
    rsi_timeperiods = range(10, 30, 1)
    
    total_iterations = len(upper_bounds) * len(lower_bounds) * len(rsi_timeperiods)
    progress = 0

    # Display a progress bar
    progress_bar = st.progress(0)

    # Iterate over optimization parameters
    for upper_bound in upper_bounds:
        for lower_bound in lower_bounds:
            for rsi_timeperiod in rsi_timeperiods:
                strategy_stats = optimize_strategy(upper_bound, lower_bound, rsi_timeperiod)
                progress += 1
                progress_bar.progress(progress / total_iterations)

    st.success("Optimization Complete!")

if __name__ == "__main__":
    main()
