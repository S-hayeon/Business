import streamlit as st
import requests
import pandas as pd

# Fetch data from Tiingo API
def fetch_data():
    import requests
    headers = {
    'Content-Type': 'application/json' }
    requestResponse = requests.get("https://api.tiingo.com/tiingo/crypto/prices?tickers=ltc&startDate=2019-01-02&resampleFreq=5min&token=bc908ecf0174940b54fc0841864d52642a607604", headers=headers)
    st.write(requestResponse.json())
    #return data

# Calculate arbitrage
def calculate_arbitrage(base_coin, investment_coin):
    pass
    # Fetch data for base and investment coins
    # base_data = fetch_data(base_coin)
    # investment_data = fetch_data(investment_coin)

    # # Calculate arbitrage (this is a simplified example, you'll need to implement your own logic here)
    # arbitrage = investment_data[0]['price'] - base_data[0]['price']

    # return arbitrage

# Streamlit interface
def main():
    # st.title('Crypto Arbitrage Trading App')

    # # User inputs
    # base_coin = st.selectbox('Select Base Coin', ['btcusd', 'ethusd', 'ltcusd'])
    # investment_coin = st.selectbox('Select Investment Coin', ['btcusd', 'ethusd', 'ltcusd'])

    # # Calculate arbitrage
    # arbitrage = calculate_arbitrage(base_coin, investment_coin)

    # # Display results
    # st.write(f'The arbitrage between {base_coin} and {investment_coin} is {arbitrage}')
    fetch_data()

if __name__ == "__main__":
    main()
