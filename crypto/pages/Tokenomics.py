import requests
import streamlit as st
# Define the cryptocurrency you want to scrape data for
st.title(f"{st.session_state['CurrencyPair']}:orange[ Tokenomics]")
crypto_symbol = st.session_state['Token']
# Define the CoinGecko API endpoint for the cryptocurrency
url = f"https://api.alternative.me/v2/ticker/"
# Send a GET request to the API endpoint
response = requests.get(url)
if response.status_code==200:
  token_data = response.json()
else:
  st.toast("Data Fetch Error")
value_id=None
try:
  for key,value in token_data['data'].items():
    if value.get('symbol')==crypto_symbol:
      value_id=value['id']
      tokenomics_data=token_data['data'][str(value_id)]
      token_market_cap=tokenomics_data['quotes']['USD']['market_cap']
      token_total_supply=tokenomics_data['total_supply']
      token_max_supply=tokenomics_data['max_supply']
      token_circulating_supply=tokenomics_data['circulating_supply']
      st.write(f"${crypto_symbol} Market Cap in $USD:{token_market_cap}")
      st.write(f"${crypto_symbol} 24hr Total Supply:{token_total_supply}")
      st.write(f"${crypto_symbol} 24hr Max Supply:{token_max_supply}")
      st.write(f"${crypto_symbol} 24hr Circulating Supply:{token_circulating_supply}")
except:
  st.toast("Coin Pair Tokenomics not available")

