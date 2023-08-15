
import ta_py as ta
import talib
class Pattern:
    def __init__(self, data):
        self.data = data
        self.max_pattern=None
        self.max_value=None
        self.trend=None
        self.candlestick_dict = {
    'CDL2CROWS': 'Two Crows',
    'CDL3BLACKCROWS': 'Three Black Crows',
    'CDL3INSIDE': 'Three Inside Up/Down',
    'CDL3LINESTRIKE': 'Three-Line Strike',
    'CDL3OUTSIDE': 'Three Outside Up/Down',
    'CDL3STARSINSOUTH': 'Three Stars In The South',
    'CDL3WHITESOLDIERS': 'Three White Soldiers',
    'CDLABANDONEDBABY': 'Abandoned Baby',
    'CDLADVANCEBLOCK': 'Advance Block',
    'CDLBELTHOLD': 'Belt-hold',
    'CDLBREAKAWAY': 'Breakaway',
    'CDLCLOSINGMARUBOZU': 'Closing Marubozu',
    'CDLCONCEALBABYSWALL': 'Concealing Baby Swallow',
    'CDLCOUNTERATTACK': 'Counterattack',
    'CDLDARKCLOUDCOVER': 'Dark Cloud Cover',
    'CDLDOJI': 'Doji',
    'CDLDOJISTAR': 'Doji Star',
    'CDLDRAGONFLYDOJI': 'Dragonfly Doji',
    'CDLENGULFING': 'Engulfing Pattern',
    'CDLEVENINGDOJISTAR': 'Evening Doji Star',
    'CDLEVENINGSTAR': 'Evening Star',
    'CDLGAPSIDESIDEWHITE': 'Up/Down Gap Side-by-Side White Lines',
    'CDLGRAVESTONEDOJI': 'Gravestone Doji',
    'CDLHAMMER': 'Hammer',
    'CDLHANGINGMAN': 'Hanging Man',
    'CDLHARAMI': 'Harami',
    'CDLHARAMICROSS': 'Harami Cross',
    'CDLHIGHWAVE': 'High-Wave Candle',
    'CDLHIKKAKE': 'Hikkake Pattern',
    'CDLHIKKAKEMOD': 'Modified Hikkake Pattern',
    'CDLHOMINGPIGEON': 'Homing Pigeon',
    'CDLIDENTICAL3CROWS': 'Identical Three Crows',
    'CDLINNECK': 'In-Neck Pattern',
    'CDLINVERTEDHAMMER': 'Inverted Hammer',
    'CDLKICKING': 'Kicking',
    'CDLKICKINGBYLENGTH': 'Kicking - bull/bear determined by the longer marubozu',
    'CDLLADDERBOTTOM': 'Ladder Bottom',
    'CDLLONGLEGGEDDOJI': 'Long-Legged Doji',
    'CDLLONGLINE': 'Long Line Candle',
    'CDLMARUBOZU': 'Marubozu',
    'CDLMATCHINGLOW': 'Matching Low',
    'CDLMATHOLD': 'Mat Hold',
    'CDLMORNINGDOJISTAR': 'Morning Doji Star',
    'CDLMORNINGSTAR': 'Morning Star',
    'CDLONNECK': 'On-Neck Pattern',
    'CDLPIERCING': 'Piercing Pattern',
    'CDLRICKSHAWMAN': 'Rickshaw Man',
    'CDLRISEFALL3METHODS': 'Rising/Falling Three Methods',
    'CDLSEPARATINGLINES': 'Separating Lines',
    'CDLSHOOTINGSTAR': 'Shooting Star',
    'CDLSHORTLINE': 'Short Line Candle',
    'CDLSPINNINGTOP': 'Spinning Top',
    'CDLSTALLEDPATTERN': 'Stalled Pattern',
    'CDLSTICKSANDWICH': 'Stick Sandwich',
    'CDLTAKURI': 'Takuri (Dragonfly Doji with very long lower shadow)',
    'CDLTASUKIGAP': 'Tasuki Gap',
    'CDLTHRUSTING': 'Thrusting Pattern',
    'CDLTRISTAR': 'Tristar Pattern',
    'CDLUNIQUE3RIVER': 'Unique 3 River',
    'CDLUPSIDEGAP2CROWS': 'Upside Gap Two Crows',
    'CDLXSIDEGAP3METHODS': 'Upside/Downside Gap Three Methods'
}

        

    def support_resistance(self, lookback=None):
        # If lookback is None, use the default value of 15
        dataframeLength=len(self.data)
        if lookback is None:
            lookback = 25
        #lookbackPeriod=(lookback/100)*dataframeLength
        lookbackPeriod=dataframeLength
        # Calculate support and resistance levels using ta-py module
        recent_low = ta.recent_low(self.data['Low'], lookbackPeriod)
        recent_high = ta.recent_high(self.data['High'],lookbackPeriod)

        self.support = ta.support(self.data['Low'], recent_low)
        self.resistance = ta.resistance(self.data['High'], recent_high)

        #return self.support['lowest'], self.resistance['highest']
        return self.support['calculate'](len(self.data)-self.support['index']), self.resistance['calculate'](len(self.data)-self.resistance['index'])
    def candlestick_Pattern(self,index):
        self.index=index
        """
        Identifies the candlestick pattern at the specified self.index using talib.
        Identifies the candlestick trend at the specified self.index using talib.
    
        Parameters:
            self.data (pd.DataFrame): A DataFrame containing OHLC (Open, High, Low, Close) self.data.
            self.index (int): The self.index at which to identify the candlestick pattern.
    
        Returns:
            str: The identified candlestick pattern, or 'None' if no pattern is found.
        """
        if self.index >= len(self.data) or self.index < 0:
            return "Invalid self.index"
    
        # Extract OHLC self.data from DataFrame
        open_prices = self.data['Open'].values.astype(float)
        high_prices = self.data['High'].values.astype(float)
        low_prices = self.data['Low'].values.astype(float)
        close_prices = self.data['Close'].values.astype(float)
    
        # Make sure we have enough self.data to compute the candlestick pattern
        if len(open_prices) < 2:
            return "Not enough self.data to identify the candlestick pattern."
    
        # Calculate the candlestick pattern using talib
        patterns = talib.get_function_groups()['Pattern Recognition']
        #bullish_patterns=['CDLHAMMER','CDLINVERTEDHAMMER','CDLMORNINGSTAR','CDLDRAGONFLYDOJI']
        result = {}
        for pattern in patterns:
            pattern_function = getattr(talib, pattern)
            result[pattern] = pattern_function(open_prices, high_prices, low_prices, close_prices)
    
        # Get the pattern at the specified self.index
        pattern_at_index = {}
        for pattern, values in result.items():
            if values[self.index] != 0:
                pattern_at_index[pattern] = values[self.index]
    
        # Return the identified pattern
        if pattern_at_index:
            #print(pattern_at_index)
            self.max_pattern = max(pattern_at_index, key=pattern_at_index.get) # Most relevant or significant pattern among the ones identified
            #self.max_pattern = pattern_at_index[0]
            #print(self.max_pattern)
            self.max_value = pattern_at_index[self.max_pattern] #Strength of the respective candlestick pattern. Positive: 100, Negative:-100, Uncertain:0
            if self.max_value==100:
                self.trend="Bullish"
            elif self.max_value==-100:
                self.trend= "Bearish"
            elif self.max_value==0:
                self.trend= "Uncertain"
            else:
                pass
        return [self.max_pattern,self.max_value,self.trend]
            #return [self.max_pattern,self.max_value]
            #return self.max_pattern
