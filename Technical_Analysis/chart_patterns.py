# Patterns
import ta_py as ta
class Pattern:
    def __init__(self, data):
        self.data = data
    def support_resistance(self):
        # Calculate support and resistance levels using ta-py module
        lookback = 15; # No lower values after 4 periods? resets after each new low
        recent_low=ta.recent_low(self.data['Low'],lookback)
        lookback = 15; # No lower values after 4 periods? resets after each new low
        recent_high=ta.recent_high(self.data['High'],lookback)
        self.support = ta.support(self.data['Low'],recent_low)
        #self.data['resistance'] = ta.volatility.resistance(self.data['Close'], n=10, percentage=3)
        self.resistance = ta.resistance(self.data['High'],recent_high)
        return self.support['lowest'],self.resistance['highest']
