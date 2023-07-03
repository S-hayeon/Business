import requests
import pandas as pd
import streamlit as st

def calculate_arbitrage(df, base_coin, investment_coin):
    filtered_df = df[(df['FROMSYMBOL'] == base_coin) & (df['TOSYMBOL'] == investment_coin)]
    filtered_df['profit_margin'] = ((filtered_df['BID'] - filtered_df['ASK']) / filtered_df['ASK']) * 100
    sorted_df = filtered_df.sort_values(by='profit_margin', ascending=False)
    return sorted_df

def main():
    st.title('CryptoCompare Arbitrage Trading')
    url = 'https://min-api.cryptocompare.com/data/pricemultifull?fsyms=*&tsyms=USD'
    response = requests.get(url)
    data = response.json()
    raw_data = data['RAW']
    df = pd.DataFrame.from_dict(raw_data).transpose()

    coins = df.index.tolist()
    base_coin = st.selectbox('Select the base coin:', coins)
    investment_coin = st.selectbox('Select the investment coin:', coins)

    sorted_df = calculate_arbitrage(df, base_coin, investment_coin)

    st.write(f"Profit margins for {base_coin} to {investment_coin}:")
    st.dataframe(sorted_df[['MARKET', 'profit_margin']])

if __name__ == '__main__':
    main()
