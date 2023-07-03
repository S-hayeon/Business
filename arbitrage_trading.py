import requests
import streamlit as st

def calculate_arbitrage(data, base_coin, investment_coin):
    filtered_data = [item for item in data if item['symbol'].endswith(base_coin) and item['symbol'].startswith(investment_coin)]
    for item in filtered_data:
        item['profit_margin'] = ((float(item['bid_price']) - float(item['ask_price'])) / float(item['ask_price'])) * 100
    sorted_data = sorted(filtered_data, key=lambda x: x['profit_margin'], reverse=True)
    return sorted_data

def main():
    st.title('Binance Arbitrage Trading')
    response = requests.get('https://api.coinmarketcap.com/v1/ticker/?limit=100')
    data = response.json()
    coins = [item['symbol'] for item in data]
    base_coin = st.selectbox('Select the base coin:', coins)
    investment_coin = st.selectbox('Select the investment coin:', coins)

    sorted_data = calculate_arbitrage(data, base_coin, investment_coin)

    st.write(f"Profit margins for {base_coin} to {investment_coin}:")
    for item in sorted_data:
        st.write(f"Symbol: {item['symbol']}, Profit Margin: {item['profit_margin']}")

if __name__ == '__main__':
    main()
