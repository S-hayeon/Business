import os
import streamlit as st
from binance import Client

api_key = st.secrets['BINANCE_API']
api_secret = st.secrets['BINANCE_SECRET']

client = Client(api_key, api_secret)

def get_available_coins():
    exchange_info = client.get_exchange_info()
    symbols = exchange_info['symbols']
    coins = set()

    for symbol in symbols:
        base_asset = symbol['baseAsset']
        quote_asset = symbol['quoteAsset']
        coins.add(base_asset)
        coins.add(quote_asset)

    return sorted(coins)

def calculate_profit_margins(klines, price):
    profit_margins = []

    for kline in klines:
        open_price = float(kline[1])
        close_price = float(kline[4])
        profit_margin = (close_price - open_price) / open_price * 100
        profit_margins.append(profit_margin)

    return profit_margins

def main():
    st.title('Binance Arbitrage Trading')
    base_coin = st.selectbox('Select the base coin:', get_available_coins())
    investment_coin = st.selectbox('Select the investment coin:', get_available_coins())
    interval = st.selectbox('Select the interval:', ['15m', '30m', '1h', '4h', '1d', '3d', '1M', '1Y'])

    ticker = client.get_symbol_ticker(symbol=f"{base_coin}{investment_coin}")
    price = float(ticker['price'])

    klines = client.get_historical_klines(symbol=f"{base_coin}{investment_coin}", interval=interval)

    profit_margins = calculate_profit_margins(klines, price)

    st.write(f"Profit margins for {base_coin} to {investment_coin} using {interval} interval:")
    st.write(profit_margins)

if __name__ == '__main__':
    main()
