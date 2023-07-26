import ta_py as ta
class Pattern:
    def __init__(self, data):
        self.data = data

    def support_resistance(self, lookback=None):
        # If lookback is None, use the default value of 15
        if lookback is None:
            lookback = 15

        # Calculate support and resistance levels using ta-py module
        recent_low = ta.recent_low(self.data['Low'], lookback)
        recent_high = ta.recent_high(self.data['High'], lookback)

        self.support = ta.support(self.data['Low'], recent_low)
        self.resistance = ta.resistance(self.data['High'], recent_high)

        return self.support['lowest'], self.resistance['highest']
