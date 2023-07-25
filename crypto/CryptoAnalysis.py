import datetime
import pandas as pd
import requests
import sys
try:
    sys.path.append('/app/business')
    from crypto import main
except:  
    sys.path.append('/mount/src/business')
    from crypto import main
#sys.path.append('/app/business/fx')

import streamlit as st

def format_key(key):
    # Split the key by underscores, capitalize each word, and join them with a space
    return " ".join(word.capitalize() for word in key.split('_'))

def coin_token_selection():
    # Coin, Token dictionary containing the keys and values for the dropdowns
    st.title("Crypto Analysis App")
    # First dropdown for selecting the Token key
    token_selected_key = st.selectbox("Select your Token Category:", [format_key(key) for key in main.crypto_tokens.keys()])
    # Convert the formatted key back to the original key with underscores
    # token_original_key = "_".join(word.lower() for word in token_selected_key.split())
    # Second dropdown showing values based on the selected key
    token_selected_value = st.selectbox("Select a Token currency:", main.crypto_tokens[token_selected_key])
    # st.write(" Coin Selected Key:", token_original_key)
    # st.write(" Coin Selected Value:", token_selected_value)
    # First dropdown for selecting the Coin key
    coin_selected_key = st.selectbox("Select your Coin Currency:", [format_key(key) for key in main.crypto_coins.keys()])
    # Convert the formatted key back to the original key with underscores
    coin_original_key = "_".join(word.lower() for word in coin_selected_key.split())
    # Second dropdown showing values based on the selected key
    coin_selected_value = st.selectbox("Select your Coin Currency Symbol:", main.crypto_coins[coin_original_key])
    # st.write(" Coin Selected Key:", coin_original_key)
    # st.write(" Coin Selected Value:", coin_selected_value)
    st.session_state['CurrencyPair'] = f"{token_selected_value}{coin_selected_value}"

def get_historical_data(symbol, interval, start_time, end_time):
    url = f"https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "startTime": start_time,
        "endTime": end_time,
        "limit": 1000  # Adjust the limit as per your requirement
    }
    response = requests.get(url, params=params)
    print("Response status code:", response.status_code)  # Print the status code of the API response
    data = response.json()
    print("Response data:", data)  # Print the data retrieved from the API
    if not data:
        st.warning("No data available for the selected duration.")
        return None
    # Convert the data into a pandas DataFrame
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    # Drop the unnecessary columns
    df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
    # Convert the timestamp from milliseconds to a datetime object
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    # Convert OHLCV values to numeric data types
    df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].apply(pd.to_numeric)
    return df

# Example usage:
coin_token_selection()
#symbol = st.session_state['CurrencyPair']
# List of intervals to choose from
intervals = ['1m', '5m', '15m', '30m', '1h', '4h', '1d']
interval = st.selectbox("Select an interval", intervals)
st.session_state['Interval']=interval
st.write(f"The Interval: {st.session_state['Interval']}")
start_date = st.date_input("Select the start date:")
st.write(f"The start date: {start_date}")
end_date = st.date_input("Select the end date:")

if start_date is not None and end_date is not None:
    # Convert start_date and end_date to datetime.datetime objects
    start_datetime = datetime.datetime.combine(start_date, datetime.datetime.min.time())
    end_datetime = datetime.datetime.combine(end_date, datetime.datetime.min.time()) + datetime.timedelta(days=1) - datetime.timedelta(milliseconds=1)
    start_time = int(start_datetime.timestamp() * 1000)  # Convert to milliseconds
    st.session_state['Start_Time']=start_time
    end_time = int(end_datetime.timestamp() * 1000)  # Convert to milliseconds
    st.session_state['End_Time']=end_time
    df = get_historical_data(st.session_state['CurrencyPair'], st.session_state['Interval'], st.session_state['Start_Time'], st.session_state['End_Time'])
    st.write(f"The start time: {start_time}")
    st.write(f"The end time: {end_time}")
    st.dataframe(df)

if st.session_state['CurrencyPair'] == '' or st.session_state['CurrencyPair'] is None:
    st.error("Select coin(s) to proceed!!")
else:
    st.write(f"Your selected coin pair for analysis is {st.session_state['CurrencyPair']}")

if st.button('Visualize Data'):
    if df is not None:
        st.write("Data exported!!")
        st.dataframe(df)
