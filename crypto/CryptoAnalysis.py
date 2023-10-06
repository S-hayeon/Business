#Import the necessary libraries
import ccxt
from datetime import datetime, timedelta
#import datetime
from io import BytesIO
import matplotlib.pyplot as plt
#from mpl_finance import candlestick_ohlc
import mplfinance as mpf
import numpy as np
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
import talib
import time
import zipfile
refresh_interval=60 # Refresh in 60 seconds
st.session_state['CoinPair']=None
st.session_state['DataFrame']=None
st.session_state['End_Date']=None
st.session_state['Start_Date']=None
cryptolist = ['BTCBUSD', 'BTCUSDT', 'ETHBUSD', 'ETHUSDT', 'BNBUSDT', 'BNBBUSD', 'XRPBUSD', 'XRPUSDT','ADABUSD', 'ADAUSDT', 'MATICBUSD', 'MATICUSDT', 'SHIBBUSD', 'SHIBUSDT', 'DOGEBUSD', 'DOGEUSDT']
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
    st.session_state['TokenName']= main.crypto_dict[token_selected_value]
    st.session_state['TokenCategory']= token_selected_key
    st.session_state['CoinPair']= f"{token_selected_value}{coin_selected_value}"
    st.sidebar.success(f"Coin pair is: {st.session_state['CoinPair']} ",icon="✅")
#@st.cache_data(ttl=3600)
# def get_historical_data(symbol, interval, start_time, end_time):
#     url = f"https://api.binance.com/api/v3/klines"
#     limit = 1000  # Number of data points per request
#     all_data = []  # To store all retrieved data

#     while start_time < end_time:
#         params = {
#             "symbol": symbol,
#             "interval": interval,
#             "startTime": start_time,
#             "endTime": end_time,
#             "limit": limit
#         }
#         response = requests.get(url, params=params)
#         st.session_state['response']=response
#         data = response.json()

#         if not data:
#             break
#         all_data.extend(data)
#         if len(data)>0:
#             start_time = int(data[-1][0]) + 1  # Set the new start_time to the next timestamp in the response

#     if not all_data:
#         st.warning("No data available for the selected duration.")
#         return None

#     # Convert all_data into a pandas DataFrame
#     df = pd.DataFrame(all_data, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
#     # Drop the unnecessary columns
#     #df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
#     # Convert the timestamp from milliseconds to a datetime object
#     df['Date'] = pd.to_datetime(df['Date'], unit='ms')
#     #df.index.name = 'Date'
#     df.set_index('Date',inplace=True)
#     # Convert OHLCV values to numeric data types
#     df[['Open', 'High', 'Low', 'Close', 'Volume']] = df[['Open', 'High', 'Low', 'Close', 'Volume']].apply(pd.to_numeric)
#     return df
# @st.cache_data()
# def get_historical_data(symbol, interval, start_time, end_time):
#     # Initialize the Binance exchange object (you can replace this with your preferred exchange)
#     exchange = ccxt.binance()

#     # Define the parameters for fetching historical data
#     params = {
#         'symbol': symbol,
#         'timeframe': interval,
#         'since': start_time,
#         'limit': 1000,  # Adjust this limit as needed
#     }

#     # Initialize an empty list to store the data
#     data = []

#     try:
#         while True:
#             # Fetch candlestick data
#             ohlcv = exchange.fetch_ohlcv(**params)

#             # If there's no more data, break the loop
#             if len(ohlcv) == 0:
#                 break

#             # Append the data to the list
#             data.extend(ohlcv)

#             # Update the 'since' parameter for the next request
#             params['since'] = ohlcv[-1][0] + 1

#             # If the next timestamp is greater than the end_time, break the loop
#             if params['since'] > end_time:
#                 break

#     except ccxt.NetworkError as e:
#         st.toast(f'Network error: {e}')
#     except ccxt.ExchangeError as e:
#         st.toast(f'Exchange error {e}')
#     except Exception as e:
#         st.toast(f'An error occurred {e}')

#     # Create a DataFrame from the fetched data
#     df = pd.DataFrame(data, columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])

#     # Convert the timestamp to a datetime format
#     df['Date'] = pd.to_datetime(df['Timestamp'], unit='ms')

#     # Reorder the columns
#     df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
#     df.set_index('Date',inplace=True)

#     return df

def format_url(symbol, type, interval, date):
    if type == 'Daily':
        base_url = 'https://data.binance.vision/data/spot/daily/klines/'
    elif type == 'Monthly':
        base_url = 'https://data.binance.vision/data/spot/monthly/klines/'
    else:
        return None

    url_formatted = f"{base_url}{symbol}/{interval}/{symbol}-{interval}-{date}.zip"
    return url_formatted

# Function to download and extract data
def download_and_extract_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        with zipfile.ZipFile(BytesIO(response.content), 'r') as zip_file:
            file_list = zip_file.namelist()
            if len(file_list) == 1:
                with zip_file.open(file_list[0]) as csv_file:
                    datatable = pd.read_csv(csv_file)
                    datatable = datatable.iloc[:, :6]  # All rows and columns up to 6
                    datatable.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
                    datatable['Date'] = pd.to_datetime(datatable['Date'], unit='ms')  # Convert 'Date' column to datetime
                    datatable = datatable.set_index('Date',inplace=True)  # Note this is in ms
                    #datatable.index = pd.to_datetime(datatable.index, unit='ms')
                    #datatable = datatable.astype(float)  # Convert values from strings to float
                return datatable
            else:
                print("Error: The .zip file contains more than one file.")
    else:
        print(f"Error: Failed to download the .zip file from {url}")
@st.cache_resource(show_spinner=True)
# Function to retrieve historical data for a date range
def get_historical_data(symbol, type, interval, start_date, end_date):
    combined_data = pd.DataFrame()
    current_date = start_date

    while current_date <= end_date:
        formatted_date = current_date.strftime('%Y-%m-%d')
        url = format_url(symbol, type, interval, formatted_date)
        
        if url:
            data = download_and_extract_data(url)
            if data is not None:
                combined_data = pd.concat([combined_data, data])
        
        current_date += timedelta(days=1)

    return combined_data
# def get_historical_data(symbol, interval, start_time, end_time):
#     klines = client.get_historical_klines(
#         symbol=symbol,
#         interval=interval,
#         start_str=start_time,
#         end_str=end_time,
#     )
#     frame=pd.DataFrame(klines)
#     frame=frame.iloc[:,:6] # All rows and column upto 6
#     # Naming the columns
#     frame.columns=['Date','Open','High','Low','Close','Volume']
#     # Name the rows
#     frame=frame.set_index('Date') # Note this is in ms
#     # Convert this Time to readable form since this is time from 1970s
#     frame.index=pd.to_datetime(frame.index,unit='ms')
#     frame=frame.astype(float) # Convert values from strings to float
#     return frame
#@st.cache_resource(show_spinner=False)
def visualize_data(df):
    # Create  placeholders
    candlestickfigure_placeholder = st.empty()
    #data_placeholder = st.empty()
    df_expander_placeholder = st.empty()
    expander_placeholder = st.empty()
    status_displayed = False  # Flag to track whether status message has been displayed
    response_placeholder = st.empty()
    # Continuously update the data by fetching new data from the API
    #while True:
    #df = get_historical_data(st.session_state['CoinPair'], st.session_state['Interval'], st.session_state['Start_Time'],st.session_state['End_Time'])
    # If data is not empty, show the data in the frontend
    if df is not None:
        #st.session_state['DataFrame']=df
        title_placeholder.header(f"{st.session_state['CurrencyPair']} Crypto Analysis")
        fig=mpf.plot(df,type='line',volume=True,style='binance')
        candlestickfigure_placeholder.pyplot(fig)
        with df_expander_placeholder.expander("View the data"):
            #data_placeholder.dataframe(df)
            st.dataframe(df)
            # Display status message only once
            if not status_displayed:
                #st.sidebar.info(f"Response status {response.status_code}")
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
def recent_tech_indicators(interval):
    # Initialize a dictionary to store DataFrames for each cryptocurrency
    crypto_data = {}
    start_date = datetime.now() - timedelta(days=3)  # Last 3 days
    end_date = datetime.now()
    # Iterate through the list of cryptocurrencies and retrieve recent data
    for symbol in cryptolist:
        data = get_historical_data(symbol,'Daily',interval,start_date, end_date)
        if data is not None:
            # Extract relevant data for ADX and RSI calculation
            high = data['High']
            low = data['Low']
            close = data['Close']
            # Calculate ADX
            adx = talib.ADX(high, low, close, timeperiod=14)
            # Calculate RSI
            rsi = talib.RSI(close, timeperiod=14)
            # Create a DataFrame for the current symbol pair
            crypto_df = pd.DataFrame({
                'Date': data.index,
                'ADX': adx,
                'RSI': rsi
            })
            # Store the DataFrame in the dictionary with the symbol as the key
            crypto_data[symbol] = crypto_df
    for symbol in cryptolist:
        coin_data = crypto_data[symbol]
        last_adx_value = coin_data['ADX'][len(coin_data)-1]
        prev_adx_value = coin_data['ADX'][len(coin_data)-2]
        if not np.isnan(last_adx_value) and not np.isnan(prev_adx_value) and last_adx_value != 0:
            adx_change=((last_adx_value-prev_adx_value)/last_adx_value)*100
        else:
            adx_change=0
        last_rsi_value = coin_data['RSI'][len(coin_data)-1]
        prev_rsi_value = coin_data['RSI'][len(coin_data)-2]
        if not np.isnan(last_rsi_value) and not np.isnan(prev_rsi_value) and last_rsi_value != 0:
            rsi_change=((last_rsi_value-prev_rsi_value)/last_rsi_value)*100
        else:
            rsi_change=0
        #st.write(f'## {coin_pair} Analysis')
        # Display coin symbol and ADX and RSI values using st.metric()
        col1, col2, col3 = st.columns(3)
        # Set the width of col1 to be wider
        col1_width = 1200  # You can adjust this value
        # Create custom CSS styles to control the column widths
        col1_style = f"width: {col1_width}px;"
        col2_style = "width: auto;"
        col3_style = "width: auto;"
        # Apply the custom styles to the columns
        col1.markdown(f'<div style="{col1_style}"></div>', unsafe_allow_html=True)
        col2.markdown(f'<div style="{col2_style}"></div>', unsafe_allow_html=True)
        col3.markdown(f'<div style="{col3_style}"></div>', unsafe_allow_html=True)
        with col1:
            st.metric("Coin Pair", symbol)
        with col2:
            st.metric("ADX",round(last_adx_value, 2),f"{round(adx_change, 2)}%")
        with col3:
            st.metric("RSI",round(last_rsi_value,2),f"{round(rsi_change,2)}%")
    
def popularCoinPrices():
    start_date = datetime.now() - timedelta(days=2)  # Last 3 days
    end_date = datetime.now()
    interval='1d'
    col1,col2,col3 =st.columns(3)
    for index, symbol in enumerate(cryptolist):
        popularcoinDF = get_historical_data(symbol,'Daily',interval,start_date, end_date)
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
        #popularCoinPrices()
        #time.sleep(3)
        coin_token_selection()
        app_title=st.empty()
        st.title(f" :blue[{st.session_state['TokenName']}] Crypto Analysis App")
        intervals = ['1m', '5m', '15m', '30m', '1h', '4h', '1d','3d','1w','1mo']
        interval = st.sidebar.selectbox("Select an interval", intervals)
        title_placeholder=st.empty()
        #st.write(f"The Interval: {st.session_state['Interval']}")
        st.session_state["Start_Date"] = st.sidebar.date_input("Select the start date:")
        st.session_state["End_Date"] = st.sidebar.date_input("Select the end date:")


        if st.session_state["Start_Date"] is not None and st.session_state["End_Date"] is not None:
            # Convert start_date and end_date to datetime.datetime objects
            # start_datetime = datetime.datetime.combine(st.session_state["Start_Date"], datetime.datetime.min.time())
            # end_datetime = datetime.datetime.combine(st.session_state["End_Date"], datetime.datetime.min.time()) + datetime.timedelta(days=1) - datetime.timedelta(milliseconds=1)
            # start_time = int(start_datetime.timestamp() * 1000)  # Convert to milliseconds
            # start_time_formatted = datetime.datetime.fromtimestamp(start_time / 1000.0).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            # end_time = int(end_datetime.timestamp() * 1000)  # Convert to milliseconds
            # end_time_formatted = datetime.datetime.fromtimestamp(end_time / 1000.0).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            #df = get_historical_data(st.session_state['CurrencyPair'], st.session_state['Interval'], st.session_state['Start_Time'], st.session_state['End_Time'])
            #st.write(f"The start time: {start_time}")
            #st.write(f"The end time: {end_time}")
            #st.dataframe(df)
            pass
        if st.sidebar.button('Start Analysis'):
            st.cache_data.clear()
            st.session_state['CurrencyPair']=st.session_state['CoinPair']
            st.session_state['Interval']=interval
            #st.session_state['Start_Time']=start_time
            #st.session_state['End_Time']=end_time
            if st.session_state['CurrencyPair'] is not None:
                @st.cache_resource()
                def get_cached_data(coin_pair, interval, start_date, end_date):
                    return get_historical_data(coin_pair, 'Daily', interval, start_date, end_date)
                # Call the cached function
    
                # Convert the datetime.date object to a string
                start_date_str = st.session_state['Start_Date'].strftime('%Y-%m-%d')
                # Parse the string into a datetime.datetime object
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                end_date_str = st.session_state['End_Date'].strftime('%Y-%m-%d')
                # Parse the string into a datetime.datetime object
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                df = get_cached_data(st.session_state['CoinPair'], st.session_state['Interval'], start_date,end_date)
                #df = get_historical_data(st.session_state['CoinPair'],'Daily',st.session_state['Interval'], st.session_state['Start_Date'],st.session_state['End_Date']).returnDF()
                st.toast("Successful Data Refresh",icon='😍')
                visualize_data(df)
                st.session_state['DataFrame']=df
            else:
                st.error("Choose a Coin")
        if st.sidebar.button("Start Technical Analysis"):
           with st.expander("Indicators Change in %"):
              recent_tech_indicators(interval)
	
        st.set_option('deprecation.showPyplotGlobalUse', False)
