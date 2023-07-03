
import streamlit as st
import requests
import pandas as pd

# Fetching the data
def fetch_data():
    url = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit=10&sortBy=market_cap&sortType=desc&convert=USD,BTC,ETH&cryptoType=all&tagType=all&audited=false"
    response = requests.get(url)
    data = response.json()
    print(data)  # Print the data to the console
    return data

# Calculating the arbitrage
def calculate_arbitrage(base_coin, investment_coin, data):
    # Find the base coin and investment coin in the data
    base_coin_data = next((coin for coin in data['data']['cryptoCurrencyList'] if coin['name'] == base_coin), None)
    investment_coin_data = next((coin for coin in data['data']['cryptoCurrencyList'] if coin['name'] == investment_coin), None)

    # Check if the coins were found
    if base_coin_data is None or investment_coin_data is None:
        return None

    # Calculate the arbitrage (this is a simplified example and might not reflect the actual profit)
    arbitrage = investment_coin_data['quote']['USD']['price'] - base_coin_data['quote']['USD']['price']

    return arbitrage

# Streamlit application
def main():
    st.title("MarketCap Arbitrage Trading Application")

    # Fetching the data
    try:
        data = fetch_data()
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")
        return

    # Creating the dropdown menus
    base_coin = st.selectbox("Select Base Coin", options=[coin['name'] for coin in data['data']['cryptoCurrencyList']])
    investment_coin = st.selectbox("Select Investment Coin", options=[coin['name'] for coin in data['data']['cryptoCurrencyList']])
    time_interval = st.selectbox("Select Time Interval", options=['15min', '30min', '1hr', '4hr', '1day', '3day', '1month', '1year'])

    # Calculating the arbitrage
    arbitrage = calculate_arbitrage(base_coin, investment_coin, data)

    # Check if the arbitrage calculation was successful
    if arbitrage is None:
        st.error("Failed to calculate arbitrage. Please make sure the selected coins are correct.")
        return

    # Displaying the results
    st.write(f"The arbitrage is: {arbitrage}")

if __name__ == "__main__":
    main()
