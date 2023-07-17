class TechnicalAnalysis:
  def technicalIndicators(self):
    import numpy as np
    import talib
    c=np.random.randn(100)
    k,b=talib.STOCHRSI(c)
    return k,b
