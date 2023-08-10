Skip to content
Dre-AsiliVentures
/
Business

Type / to search

Code
Issues
Pull requests
Actions
Projects
Wiki
Security
Insights
Settings
BreadcrumbsBusiness/crypto
/
CryptoAnalysis.py
in
main

Edit

Preview
Indent mode

Spaces
Indent size

4
Line wrap mode

No wrap
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
        while remaining_time > 0:
            response_placeholder.info(f"For accuracy, data will refresh in {remaining_time} seconds")
            remaining_time -= 1
            time.sleep(1)  # Wait for 1 second
        st.cache_data.clear()
        
        # Sleep for 60 seconds before fetching new data again
        #time.sleep(60)

# Main loop
def round_value(input_value):
    if input_value>1:
        a=round(input_value,3) # Round values above 1 to 3 decimal places
    else:
        a=round(input_value,8) # Round values less than 1 to 8 decimal places
    return a
def popularCoinPrices():
    # Fetch data from the API
    while True:
        url='https://data.binance.com/api/v3/ticker/24hr'
        popularcoinDF = pd.DataFrame(requests.get(url).json())
        
        cryptolist = ['BTCBUSD', 'BTCUSDT', 'ETHBUSD', 'ETHUSDT', 'BNBUSDT', 'BNBBUSD', 'XRPBUSD', 'XRPUSDT',
                      'ADABUSD', 'ADAUSDT', 'MATICBUSD', 'MATICUSDT', 'SHIBBUSD', 'SHIBUSDT', 'DOGEBUSD', 'DOGEUSDT']
        
        col1,col2,col3 =st.columns(3)
        for index, symbol in enumerate(cryptolist):
            crypto_df = popularcoinDF[popularcoinDF.symbol == symbol]
            crypto_price = round_value(float(crypto_df.weightedAvgPrice))
            crypto_percent = f'{float(crypto_df.priceChangePercent)}%'  # the :.2f specifies the floating point number to 2 decimal places
            #print("{} {} {}".format(symbol, crypto_price, crypto_percent))
            if index % 3 == 0:
                col=col1
            elif index%3==1:
                col=col2
            else:
                col=col3
            with col:
                st.metric(symbol,crypto_price, crypto_percent)
        time.sleep(60) # Wait every 60 seconds then update
@st.cache_data
def realtime_prices():
    realtime_prices=threading.Thread(target=popularCoinPrices)
    realtime_prices.start()
if __name__=='__main__':
    realtime_prices()
    coin_token_selection()
    intervals = ['1m', '5m', '15m', '30m', '1h', '4h', '1d']
    interval = st.sidebar.selectbox("Select an interval", intervals)
    #st.write(f"The Interval: {st.session_state['Interval']}")
    start_date = st.sidebar.date_input("Select the start date:")
    #st.write(f"The start date: {start_date}")
    end_date = st.sidebar.date_input("Select the end date:")
    
    if start_date is not None and end_date is not None:
        # Convert start_date and end_date to datetime.datetime objects
        start_datetime = datetime.datetime.combine(start_date, datetime.datetime.min.time())
        end_datetime = datetime.datetime.combine(end_date, datetime.datetime.min.time()) + datetime.timedelta(days=1) - datetime.timedelta(milliseconds=1)
        start_time = int(start_datetime.timestamp() * 1000)  # Convert to milliseconds
        end_time = int(end_datetime.timestamp() * 1000)  # Convert to milliseconds
        #df = get_historical_data(st.session_state['CurrencyPair'], st.session_state['Interval'], st.session_state['Start_Time'], st.session_state['End_Time'])
        #st.write(f"The start time: {start_time}")
        #st.write(f"The end time: {end_time}")
        #st.dataframe(df)
    if st.sidebar.button('Start Analysis'):
        st.session_state['CurrencyPair']=st.session_state['CoinPair']
        st.session_state['Interval']=interval
        st.session_state['Start_Time']=start_time
        st.session_state['End_Time']=end_time
        if st.session_state['CurrencyPair'] is not None:
            st.toast("Streaming started",icon='😍')
            visualize_data()
        else:
            st.error("Choose a Coin")
    st.set_option('deprecation.showPyplotGlobalUse', False)


