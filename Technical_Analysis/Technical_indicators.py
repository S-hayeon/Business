import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import ta_py as ta
class TIndicators:
  def __init__(self,data):
    self.data=data['Close']
    pass
  def MACD(self):
    #c=np.random.randn(100)
    length1 = 12; # default = 12
    length2 = 26; # default = 26
    length3= 9;
    macd = ta.macd(self.data, length1, length2)
    signal_line = ta.ema(self.data,length3)
    # plt.plot(macd, label='MACD Line')
    # plt.plot(signal_line, label='Signal Line')
    # plt.xlabel('Time')
    # plt.ylabel('Value')
    # plt.title('MACD and Signal Line')
    # plt.legend()
    # plt.show()
    
    # Create a new figure and axis
    fig, ax = plt.subplots()

    # Plot MACD Line and Signal Line on the same axis
    ax.plot(macd, label='MACD Line')
    ax.plot(signal_line, label='Signal Line')

    # Set axis labels and title
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')
    ax.set_title('MACD and Signal Line')

    # Show legend
    ax.legend()

    # Show the plot
    plt.show()
    st.pyplot(fig)
    # Find the index of the all time the MACD line crosses above the signal line, to find first time add [0]
    macd_cross_above_signal = macd.index[macd > signal_line]
    # Find theindex of the all time the MACD line crosses below the signal line
    macd_cross_below_signal = macd.index[macd < signal_line]
    # Print the date of the first MACD crossover
    st.write(f'The MACD line crossed above the signal line on {df.loc[macd_cross_above_signal].name}')
    # Print the date of the first MACD crossover
    st.write(f'The MACD line crossed below the signal line on {df.loc[macd_cross_below_signal].name}')
    return macd,signal_line
