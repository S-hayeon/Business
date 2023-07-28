# Import the necessary libraries
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
def format_key(key):
    # Split the key by underscores, capitalize each word, and join them with a space
    return " ".join(word.capitalize() for word in key.split('_'))

def coin_token_selection():
    # Coin, Token dictionary containing the keys and values for the dropdowns
    st.title("Crypto Analysis App")
    # First dropdown for selecting the Token key
    token_selected_key = st.sidebar.selectbox("Select your Token Category:", list(main.crypto_tokens.keys()))
    #token_selected_key = st.selectbox("Select your Token Category:", [format_key(key) for key in main.crypto_tokens.keys()])
    # Convert the formatted key back to the original key with underscores
    # token_original_key = "_".join(word.lower() for word in token_selected_key.split())
    # Second dropdown showing values based on the selected key
    token_selected_value = st.sidebar.selectbox("Select a Token currency:", main.crypto_tokens[token_selected_key])
    # st.write(" Coin Selected Key:", token_original_key)
    # st.write(" Coin Selected Value:", token_selected_value)
    # First dropdown for selecting the Coin key
    coin_selected_key = st.sidebar.selectbox("Select your Coin Currency:", [format_key(key) for key in main.crypto_coins.keys()])
    # Convert the formatted key back to the original key with underscores
    coin_original_key = "_".join(word.lower() for word in coin_selected_key.split())
    # Second dropdown showing values based on the selected key
    coin_selected_value = st.sidebar.selectbox("Select your Coin Currency Symbol:", main.crypto_coins[coin_original_key])
    # st.write(" Coin Selected Key:", coin_original_key)
    # st.write(" Coin Selected Value:", coin_selected_value)
    st.session_state['CurrencyPair'] = f"{token_selected_value}{coin_selected_value}"
    st.sidebar.write(f"Selected coin pair is {st.session_state['CurrencyPair']}")
@st.cache_data
def get_historical_data(symbol, interval, start_time, end_time):
    #url = f"https://api.binance.us/api/v3/klines"
    url = f"https://data.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "startTime": start_time,
        "endTime": end_time,
        "limit": 5000  # Adjust the limit as per your requirement
    }
    response = requests.get(url, params=params)
    st.session_state['response']=response
    data = response.json()
    print("Response data:", data)  # Print the data retrieved from the API
    if not data:
        st.warning("No data available for the selected duration.")
        return None
    # Convert the data into a pandas DataFrame
    df = pd.DataFrame(data, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    # Drop the unnecessary columns
    #df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
    # Convert the timestamp from milliseconds to a datetime object
    df['Date'] = pd.to_datetime(df['Date'], unit='ms')
    #df.index.name = 'Date'
    df.set_index('Date',inplace=True)
    # Convert OHLCV values to numeric data types
    df[['Open', 'High', 'Low', 'Close', 'Volume']] = df[['Open', 'High', 'Low', 'Close', 'Volume']].apply(pd.to_numeric)
    return df
@st.cache_resource
def visualize_data():
    # Get the current selected coin pair and interval
    symbol = st.session_state['CurrencyPair']
    interval = st.session_state['Interval']
    #fig=plt.style.use('ggplot')


    # Check if the current coin pair and interval are not empty and not None
    if symbol and interval:
        # Get the current start and end time
        start_time = st.session_state['Start_Time']
        end_time = st.session_state['End_Time']

        # Create a placeholder for the dataframe
        data_placeholder = st.empty()
        candlestickfigure_placeholder = st.empty()
        status_displayed = False  # Flag to track whether status message has been displayed
        response_placeholder = st.empty()
        # Continuously update the data by fetching new data from the API
        while True:
            df = get_historical_data(symbol, interval, start_time, end_time)
            st.session_state['DataFrame']=df

            # If data is not empty, show the data in the frontend
            if df is not None:
                # Display the dataframe inside the placeholder
                data_placeholder.dataframe(st.session_state['DataFrame'])
                # Display status message only once
                fig=mpf.plot(df,type='candle',volume=True,style='charles')
                candlestickfigure_placeholder.pyplot(fig)
                if not status_displayed:
                    response=st.session_state['response']
                    st.sidebar.info(f"Response status {response.status_code}")
                    status_displayed = True
            remaining_time = refresh_interval
            while remaining_time > 0:
                response_placeholder.info(f"For accuracy, data will refresh in {remaining_time} seconds")
                remaining_time -= 1
                time.sleep(1)  # Wait for 1 second

            # Sleep for 60 seconds before fetching new data again
            #time.sleep(60)
# Example usage:
coin_token_selection()
#symbol = st.session_state['CurrencyPair']
# List of intervals to choose from
intervals = ['1m', '5m', '15m', '30m', '1h', '4h', '1d']
interval = st.sidebar.selectbox("Select an interval", intervals)
st.session_state['Interval']=interval
#st.write(f"The Interval: {st.session_state['Interval']}")
start_date = st.sidebar.date_input("Select the start date:")
#st.write(f"The start date: {start_date}")
end_date = st.sidebar.date_input("Select the end date:")

if start_date is not None and end_date is not None:
    # Convert start_date and end_date to datetime.datetime objects
    start_datetime = datetime.datetime.combine(start_date, datetime.datetime.min.time())
    end_datetime = datetime.datetime.combine(end_date, datetime.datetime.min.time()) + datetime.timedelta(days=1) - datetime.timedelta(milliseconds=1)
    start_time = int(start_datetime.timestamp() * 1000)  # Convert to milliseconds
    st.session_state['Start_Time']=start_time
    end_time = int(end_datetime.timestamp() * 1000)  # Convert to milliseconds
    st.session_state['End_Time']=end_time
    #df = get_historical_data(st.session_state['CurrencyPair'], st.session_state['Interval'], st.session_state['Start_Time'], st.session_state['End_Time'])
    #st.write(f"The start time: {start_time}")
    #st.write(f"The end time: {end_time}")
    #st.dataframe(df)
if st.sidebar.button('Start Analysis'):
    if st.session_state['CurrencyPair'] is not None:
        st.sidebar.write("Streaming started!!")
        #st.dataframe(df)
        visualize_data()
        # Run the visualize_data function using st.experimental_streamlit_request
        #st.experimental_streamlit_request(visualize_data())
    else:
        st.error("Choose a Coin")
st.set_option('deprecation.showPyplotGlobalUse', False)

