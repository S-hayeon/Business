
import ta_py as ta
class Pattern:
    def __init__(self, data):
        self.data = data

    def support_resistance(self, lookback=None):
        # If lookback is None, use the default value of 15
        dataframeLength=len(self.data)
        if lookback is None:
            lookback = 25
        lookbackPeriod=(lookback/100)*dataframeLength
        # Calculate support and resistance levels using ta-py module
        recent_low = ta.recent_low(self.data['Low'], lookbackPeriod)
        recent_high = ta.recent_high(self.data['High'],lookbackPeriod)

        self.support = ta.support(self.data['Low'], recent_low)
        self.resistance = ta.resistance(self.data['High'], recent_high)

        return self.support['lowest'], self.resistance['highest']
