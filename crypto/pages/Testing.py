from backtesting import Backtest, Strategy
from backtesting.test import GOOG
import streamlit as st
import time
import backtesting  # Import your backtesting library

def optimize_strategy():
    class RSIOscillator(Strategy):
      upper_bound = 70
      lower_bound = 30
      rsi_timeperiod=14
      def init(self):
        self.rsi = self.I(talib.RSI, self.data.Close,self.rsi_timeperiod)
      def next(self):
        if self.rsi[-1] > self.upper_bound and self.data.Close[-1]<self.ema[-1]:
          self.position.close()
        elif self.rsi[-1] < self.lower_bound and self.data.Close[-1]>self.ema[-1]:
          self.buy()
    bt=Backtest(GOOG,RSIOscillator,cash=10_000)
    strategyStats=bt.optimize(
    upper_bound=range(50,85,5), # Optimize Upper bound from 50-85 in steps of 5
    lower_bound=range(10,50,5), # Optimize Lower bound from 10-50 in steps of 5
    rsi_timeperiod=range(10,30,1), # Optimize the strategy with RSI timeperiod betweeen 10 and 30 in steps of 2
)

def main():
    st.title("Backtesting Optimization Progress")

    # Display a progress bar
    progress_bar = st.progress(0)

    # Run the optimization and update progress bar
    for progress in optimize_strategy():
        progress_bar.progress(progress)
    
    st.success("Optimization Complete!")

if __name__ == "__main__":
    main()
