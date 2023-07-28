import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import talib
import ta_py as ta
class TIndicators:
  def __init__(self,data):
    self.df=data
    self.data=data['Close']
    self.sma_50 = 0
    self.sma_200 = 0
    self.rsi = 0
    self.macd = 0
    self.signal = 0
    self.adx = 0

    # State variables
    self.sma_50_greater_than_sma_200 = None
    self.rsi_above_70 = None
    self.macd_above_signal = None
    self.adx_above_25 = None
    self.rsi_below_30 = None
    self.macd_below_signal = None
    self.rsi_below_20 = None

  def MACD(self):
    length1 = 12; # default = 12
    length2 = 26; # default = 26
    length3= 9;
    macd_array = ta.macd(self.data.values, length1, length2)
    signal_line_array = ta.ema(self.data.values,length3)
    # Create a new figure and axis
    fig, ax = plt.subplots()
    # Plot MACD Line and Signal Line on the same axis
    ax.plot(macd_array, label='MACD Line')
    ax.plot(signal_line_array, label='Signal Line')
    # Set axis labels and title
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')
    ax.set_title('MACD and Signal Line')
    # Show legend
    ax.legend()
    # Show the plot
    plt.show()
    st.pyplot(fig)
  
    # Convert the MACD array into a pandas Series
    # macd = pd.Series(macd_array)
    # # Convert the signal line array into a pandas Series
    # signal_line = pd.Series(signal_line_array)
    # # Find the index of the all time the MACD line crosses above the signal line, to find first time add [0]
    # macd_cross_above_signal = macd.index[macd > signal_line]
    # # Find theindex of the all time the MACD line crosses below the signal line
    # macd_cross_below_signal = macd.index[macd < signal_line]
    # # Print the date of the first MACD crossover
    # st.write(f'The MACD line crossed above the signal line on {df.loc[macd_cross_above_signal].name}')
    # # Print the date of the first MACD crossover
    # st.write(f'The MACD line crossed below the signal line on {df.loc[macd_cross_below_signal].name}')
    return macd_array,signal_line_array
  def BullBearish_state(self):
      # Calculate technical indicators
      if len(self.data)>=250:
        self.sma_50 = talib.SMA(self.data, timeperiod=50)
        self.sma_200 = talib.SMA(self.data, timeperiod=200)
        self.rsi = talib.RSI(self.data)
        self.macd, self.signal, _ = talib.MACD(self.data)
        self.adx = talib.ADX(self.df['High'],self.df['Low'],self.data,timeperiod=14)
        # Splitting each condition into separate boolean variables
        self.sma_50_greater_than_sma_200 = self.sma_50.tail().all() > self.sma_200.tail().all()
        self.rsi_above_70 = self.rsi.tail().all() > 70
        self.macd_above_signal = self.macd.tail().all() > self.signal.tail().all()
        self.adx_above_25 = self.adx.tail().all() > 25
        self.rsi_below_30 = self.rsi.tail().all() < 30
        self.macd_below_signal = self.macd.tail().all() < self.signal.tail().all()
        self.rsi_below_20 = self.rsi.tail().all() < 20
        if self.sma_50_greater_than_sma_200:
            st.write(f"SMA 50 is greater than SMA 200: {self.sma_50_greater_than_sma_200}")
        else:
            st.write(f"SMA 50 is greater than SMA 200: {self.sma_50_greater_than_sma_200}")
        if self.rsi_above_70:
            st.write(f"RSI is above 70: {self.rsi_above_70}")
        else:
            st.write(f"RSI is above 70: {self.rsi_above_70}")
    
        if self.macd_above_signal:
            st.write(f"MACD is above Signal: {self.macd_above_signal}")
        else:
            st.write(f"MACD is above Signal: {self.macd_above_signal}")
    
        if self.adx_above_25:
            st.write(f"ADX is above 25: {self.adx_above_25}")
        else:
            st.write(f"ADX is above 25: {self.adx_above_25}")
    
        if self.rsi_below_30:
            st.write(f"RSI is below 30: {self.rsi_below_30}")
        else:
            st.write(f"RSI is below 30: {self.rsi_below_30}")
    
        if self.macd_below_signal:
            st.write(f"MACD is below Signal: {self.macd_below_signal}")
        else:
            st.write(f"MACD is below Signal: {self.macd_below_signal}")
    
        if self.rsi_below_20:
            st.write(f"RSI is below 20: {self.rsi_below_20}")
        else:
            st.write(f"RSI is below 20: {self.rsi_below_20}")
    
        # Return the trend classification
        if self.sma_50_greater_than_sma_200 or self.rsi_above_70 or self.macd_above_signal or self.adx_above_25:
            return "Strong Bullish"
        elif self.sma_50_greater_than_sma_200 or self.rsi_below_30 or self.macd_below_signal or self.adx_above_25:
            return "Strong Bearish"
        elif self.sma_50_greater_than_sma_200 or self.rsi_above_70 or self.macd_above_signal:
            return "Weak Bullish"
        elif self.sma_50_greater_than_sma_200 or self.rsi_below_20 or self.macd_below_signal:
            return "Weak Bearish"
        else:
            return "Neutral"
      

