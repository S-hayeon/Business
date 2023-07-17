class TechnicalAnalysis:
  def __init__(self):
    pass
  def technicalIndicators(self):
    import numpy as np
    import ta_py as ta
    c=np.random.randn(100)
    length1 = 3; # default = 12
    length2 = 6; # default = 26
    k=ta.macd(c, length1, length2)
    return k
