import matplotlib.pyplot as plt
import numpy as np
import ta_py as ta
class TIndicators:
  def __init__(self,data):
    self.data=data
    pass
  def MACD(self):
    #c=np.random.randn(100)
    length1 = 12; # default = 12
    length2 = 26; # default = 26
    length3= 9;
    macd = ta.macd(self.data, length1, length2)
    signal_line = ta.ema(self.data,length3)
    plt.plot(macd, label='MACD Line')
    plt.plot(signal_line, label='Signal Line')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title('MACD and Signal Line')
    plt.legend()
    plt.show()

    # Check for crossovers between MACD and Signal Line
    for i in range(1, len(macd)):
      if macd[i] > signal_line[i] and macd[i - 1] <= signal_line[i - 1]:
        print("MACD Line crossed above Signal Line at index", i)
      elif macd[i] < signal_line[i] and macd[i - 1] >= signal_line[i - 1]:
        print("MACD Line crossed below Signal Line at index", i)
    return macd,signal_line
