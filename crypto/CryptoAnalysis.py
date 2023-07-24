#CryptoAnalysis.py
import pandas as pd
import requests
import sys
sys.path.append('/app/business')
#sys.path.append('/app/business/fx')
from crypto import main
import streamlit as st

def format_key(key):
  # Split the key by underscores, capitalize each word, and join them with a space
  return " ".join(word.capitalize() for word in key.split('_'))
def coin_token_selection():
  # Coin, Token dictionary containing the keys and values for the dropdowns
  my_dictionary = {
      'citrus_fruits': ['Orange', 'Lemon', 'Grapefruit'],
      'tropical_fruits': ['Pineapple', 'Mango', 'Coconut'],
      'leafy_vegetables': ['Spinach', 'Kale', 'Lettuce']
  }
  st.title("Crypto Analysis App")
  # First dropdown for selecting the Token key
  token_selected_key = st.selectbox("Select your Token Category:", [format_key(key) for key in main.crypto_tokens.keys()])
  # Convert the formatted key back to the original key with underscores
  token_original_key = "_".join(word.lower() for word in coin_selected_key.split())
  # Second dropdown showing values based on the selected key
  token_selected_value = st.selectbox("Select a Token currency:", main.crypto_tokens[coin_original_key])
  st.write(" Coin Selected Key:", token_original_key)
  st.write(" Coin Selected Value:", token_selected_value)
  # First dropdown for selecting the Coin key
  coin_selected_key = st.selectbox("Select your Coin Currency:", [format_key(key) for key in main.crypto_coins.keys()])
  # Convert the formatted key back to the original key with underscores
  coin_original_key = "_".join(word.lower() for word in coin_selected_key.split())
  # Second dropdown showing values based on the selected key
  coin_selected_value = st.selectbox("Select your Coin Currency Symbol:", main.crypto_coins[coin_original_key])
  st.write(" Coin Selected Key:", coin_original_key)
  st.write(" Coin Selected Value:", coin_selected_value)
  st.session_state["CurrencyPair"]=f"{token_selected_value}{coin_selected_value}"
def get_historical_data(symbol, interval, limit=500, start_time=None, end_time=None):
    base_url = 'https://api.binance.com/api/v1/klines'
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }
    
    if start_time is not None:
        params['startTime'] = start_time
    if end_time is not None:
        params['endTime'] = end_time
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data. Status code: {response.status_code}")
        return None
   #Example usage:
symbol = st.session_state["CurrencyPair"]     # Replace with the desired trading pair symbol, e.g., BTCUSDT, ETHBTC, etc.
interval = '1h'        # Replace with the desired interval: 1m, 5m, 15m, 1h, 1d, etc.
limit = 1000           # The number of data points to retrieve (max 1000)
start_time = 1629216000000   # Replace with the desired start time in milliseconds (Unix timestamp)
end_time = 1629302400000     # Replace with the desired end time in milliseconds (Unix timestamp)
historical_data = get_historical_data(symbol, interval, limit, start_time, end_time)
# Convert the data into a pandas DataFrame
df = pd.DataFrame(historical_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
# Drop the unnecessary columns
df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
# Convert the timestamp from milliseconds to a datetime object
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
# Convert OHLCV values to numeric data types
df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].apply(pd.to_numeric)
st.dataframe(df)
