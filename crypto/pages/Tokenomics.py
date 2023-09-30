import requests
import streamlit as st
# Define the cryptocurrency you want to scrape data for
st.title(f"{st.session_state['CurrencyPair']} :orange[Tokenomics]")
crypto_symbol = "bitcoin"
# Define the CoinGecko API endpoint for the cryptocurrency
url = f"https://api.coingecko.com/api/v3/coins/{crypto_symbol}"
# Send a GET request to the API endpoint
response = requests.get(url)
crypto_data = response.json()
btc_total_supply=crypto_data['market_data']['total_supply']
btc_max_supply=crypto_data['market_data']['max_supply']
btc_circulating_supply=crypto_data['market_data']['circulating_supply']
st.write(f"$BTC 24hr Total Supply:{btc_total_supply}")
st.write(f"$BTC 24hr Max Supply:{btc_max_supply}")
st.write(f"$BTC 24hr Circulating Supply:{btc_circulating_supply}")
