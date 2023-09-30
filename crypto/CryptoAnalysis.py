#Import the necessary libraries
import datetime
import matplotlib.pyplot as plt
#from mpl_finance import candlestick_ohlc
import mplfinance as mpf
import pandas as pd
import requests
#from streamlit import caching
import streamlit as st
import sys
try:
    sys.path.append('/app/business')
    from crypto import main
except:  
    sys.path.append('/mount/src/business')
    from crypto import main
#sys.path.append('/app/business/fx')
import time
refresh_interval=60 # Refresh in 60 seconds
st.session_state['CurrencyPair']=None
st.session_state['DataFrame']=None
st.session_state['End_Date']=None
st.session_state['Start_Date']=None
def format_key(key):
    # Split the key by underscores, capitalize each word, and join them with a space
    return " ".join(word.capitalize() for word in key.split('_'))
def coin_token_selection():
    # Coin, Token dictionary containing the keys and values for the dropdowns
    # First dropdown for selecting the Token key
    token_selected_key = st.sidebar.selectbox("Select your Token Category:", list(sorted(main.crypto_tokens.keys())))
    token_selected_value = st.sidebar.selectbox("Select a Token currency:", sorted(main.crypto_tokens[token_selected_key]))

    coin_selected_key = st.sidebar.selectbox("Select your Coin Currency:", [format_key(key) for key in main.crypto_coins.keys()])
    # Convert the formatted key back to the original key with underscores
    coin_original_key = "_".join(word.lower() for word in coin_selected_key.split())
    # Second dropdown showing values based on the selected key
    coin_selected_value = st.sidebar.selectbox("Select your Coin Currency Symbol:", main.crypto_coins[coin_original_key])
    st.session_state['Token']= token_selected_value
    st.session_state['TokenCategory']= token_selected_key
    st.session_state['CoinPair']= f"{token_selected_value}{coin_selected_value}"
    st.sidebar.success(f"Coin pair is: {st.session_state['CoinPair']} ",icon="✅")

# @st.cache_data(ttl=3600) # Cache data for 1hr
# def get_historical_data(symbol, interval, start_time, end_time):
#     #url = f"https://api.binance.us/api/v3/klines"
#     url = f"https://data.binance.com/api/v3/klines"
#     params = {
#         "symbol": symbol,
#         "interval": interval,
#         "startTime": start_time,
#         "endTime": end_time,
#         "limit": 500000  # Adjust the limit as per your requirement
#     }
#     response = requests.get(url, params=params)
#     st.session_state['response']=response
#     data = response.json()
#     print("Response data:", data)  # Print the data retrieved from the API
#     if not data:
#         st.warning("No data available for the selected duration.")
#         return None
#     # Convert the data into a pandas DataFrame
#     df = pd.DataFrame(data, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
#     # Drop the unnecessary columns
#     #df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
#     # Convert the timestamp from milliseconds to a datetime object
#     df['Date'] = pd.to_datetime(df['Date'], unit='ms')
#     #df.index.name = 'Date'
#     df.set_index('Date',inplace=True)
#     # Convert OHLCV values to numeric data types
#     df[['Open', 'High', 'Low', 'Close', 'Volume']] = df[['Open', 'High', 'Low', 'Close', 'Volume']].apply(pd.to_numeric)
#     return df
#@st.cache_data(ttl=3600)
@st.cache_data
def get_historical_data(symbol, interval, start_time, end_time):
    url = f"https://data.binance.com/api/v3/klines"
    limit = 1000  # Number of data points per request
    all_data = []  # To store all retrieved data

    while start_time < end_time:
        params = {
            "symbol": symbol,
            "interval": interval,
            "startTime": start_time,
            "endTime": end_time,
            "limit": limit
        }
        response = requests.get(url, params=params)
        st.session_state['response']=response
        data = response.json()

        if not data:
            break

        all_data.extend(data)
        start_time = int(data[-1][0]) + 1  # Set the new start_time to the next timestamp in the response

    if not all_data:
        st.warning("No data available for the selected duration.")
        return None

    # Convert all_data into a pandas DataFrame
    df = pd.DataFrame(all_data, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    # Drop the unnecessary columns
    #df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
    # Convert the timestamp from milliseconds to a datetime object
    df['Date'] = pd.to_datetime(df['Date'], unit='ms')
    #df.index.name = 'Date'
    df.set_index('Date',inplace=True)
    # Convert OHLCV values to numeric data types
    df[['Open', 'High', 'Low', 'Close', 'Volume']] = df[['Open', 'High', 'Low', 'Close', 'Volume']].apply(pd.to_numeric)
    return df

#@st.cache_resource(show_spinner=False)
def visualize_data():
    # Create  placeholders
    candlestickfigure_placeholder = st.empty()
    #data_placeholder = st.empty()
    df_expander_placeholder = st.empty()
    expander_placeholder = st.empty()
    status_displayed = False  # Flag to track whether status message has been displayed
    response_placeholder = st.empty()
    # Continuously update the data by fetching new data from the API
    #while True:
    df = get_historical_data(st.session_state['CurrencyPair'], st.session_state['Interval'], st.session_state['Start_Time'],st.session_state['End_Time'])
    # If data is not empty, show the data in the frontend
    if df is not None:
        st.session_state['DataFrame']=df
        title_placeholder.header(f"{st.session_state['CurrencyPair']} Crypto Analysis")
        fig=mpf.plot(df,type='line',volume=True,style='binance')
        candlestickfigure_placeholder.pyplot(fig)
        with df_expander_placeholder.expander("View the data"):
            #data_placeholder.dataframe(df)
            st.dataframe(df)
            # Display status message only once
            if not status_displayed:
                response=st.session_state['response']
                st.sidebar.info(f"Response status {response.status_code}")
                status_displayed = True
        # Display the dataframe inside the placeholder
        with expander_placeholder.expander("Data Statistics"):
            st.markdown(f":blue[The descriptive statistics of OHLCV values:]")
            st.table(df.describe())
def round_value(input_value):
    if input_value>1:
        a=round(input_value,3) # Round values above 1 to 3 decimal
    else:
        a=round(input_value,8) # Round values less than 1 to 8 decimal places
    return a
def popularCoinPrices():
    # Fetch data from the API
    url='https://data.binance.com/api/v3/ticker/24hr'
    popularcoinDF = pd.DataFrame(requests.get(url).json())
    
    cryptolist = ['BTCBUSD', 'BTCUSDT', 'ETHBUSD', 'ETHUSDT', 'BNBUSDT', 'BNBBUSD', 'XRPBUSD', 'XRPUSDT',
                  'ADABUSD', 'ADAUSDT', 'MATICBUSD', 'MATICUSDT', 'SHIBBUSD', 'SHIBUSDT', 'DOGEBUSD', 'DOGEUSDT']
    
    col1,col2,col3 =st.columns(3)
    for index, symbol in enumerate(cryptolist):
        crypto_df = popularcoinDF[popularcoinDF.symbol == symbol]
        crypto_price = round_value(float(crypto_df.weightedAvgPrice.iloc[0]))
        crypto_percent = '{:.2f}%'.format(float(crypto_df.priceChangePercent.iloc[0]))
        #print("{} {} {}".format(symbol, crypto_price, crypto_percent))
        if index % 3 == 0:
            col=col1
        elif index%3==1:
            col=col2
        else:
            col=col3
        with col:
            st.metric(symbol,crypto_price, crypto_percent)

if __name__=='__main__':
    with st.container():
        st.title("Crypto Analysis App")
        st.header("Popular coins 24hr Prices (UTC) and Change")
        popularCoinPrices()
        title_placeholder=st.empty()
        coin_token_selection()
        intervals = ['1m', '5m', '15m', '30m', '1h', '4h', '1d']
        interval = st.sidebar.selectbox("Select an interval", intervals)
        #st.write(f"The Interval: {st.session_state['Interval']}")
        start_date = st.sidebar.date_input("Select the start date:")
        st.session_state["Start_Date"]=start_date
        #st.write(f"The start date: {start_date}")
        end_date = st.sidebar.date_input("Select the end date:")
        st.session_state["End_Date"]=end_date

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
            st.cache_data.clear()
            st.session_state['CurrencyPair']=st.session_state['CoinPair']
            st.session_state['Interval']=interval
            st.session_state['Start_Time']=start_time
            st.session_state['End_Time']=end_time
            if st.session_state['CurrencyPair'] is not None:
                st.toast("Successful Data Refresh",icon='😍')
                visualize_data()
            else:
                st.error("Choose a Coin")
        st.set_option('deprecation.showPyplotGlobalUse', False)
