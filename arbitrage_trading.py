import pandas as pd
import streamlit as st

def calculate_arbitrage(df, base_coin, investment_coin):
    filtered_df = df[(df.symbol.str.endswith(base_coin)) & (df.symbol.str.startswith(investment_coin))]
    filtered_df['profit_margin'] = ((filtered_df.bidPrice - filtered_df.askPrice) / filtered_df.askPrice) * 100
    sorted_df = filtered_df.sort_values(by='profit_margin', ascending=False)
    return sorted_df

def main():
    st.title('Binance Arbitrage Trading')
    df = pd.read_json('https://api.binance.com/api/v3/ticker/24hr')
    coins = df.symbol.str.extract(r'(\w+)(\w+)')
    coins = coins[1].unique()
    base_coin = st.selectbox('Select the base coin:', coins)
    investment_coin = st.selectbox('Select the investment coin:', coins)

    sorted_df = calculate_arbitrage(df, base_coin, investment_coin)

    st.write(f"Profit margins for {base_coin} to {investment_coin}:")
    st.dataframe(sorted_df[['symbol', 'profit_margin']])

if __name__ == '__main__':
    main()
