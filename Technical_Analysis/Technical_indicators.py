import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import talib
import ta_py as ta
class TIndicators:
  def __init__(self,data):
    self.data=data['Close']
    pass
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
    #return macd_array,signal_line_array
  def BullBearish_state(self):
    # Calculate technical indicators
    sma_50 = talib.SMA(self.data, timeperiod=50)
    sma_200 = talib.SMA(self.data, timeperiod=200)
    rsi = talib.RSI(self.data)
    macd, signal, _ = talib.MACD(self.data)
    adx = talib.ADX(self.data)
 # Determine the state
    if sma_50[-1] > sma_200[-1] and rsi[-1] > 70 and macd[-1] > signal[-1] and adx[-1] > 25:
        return "Strong Bullish"
    elif sma_50[-1] < sma_200[-1] and rsi[-1] < 30 and macd[-1] < signal[-1] and adx[-1] > 25:
        return "Strong Bearish"
    elif sma_50[-1] > sma_200[-1] and rsi[-1] > 80 and macd[-1] > signal[-1]:
        return "Weak Bullish"
    elif sma_50[-1] < sma_200[-1] and rsi[-1] < 20 and macd[-1] < signal[-1]:
        return "Weak Bearish"
    else:
        return "Neutral"

