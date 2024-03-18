from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import os
import pandas as pd 
import streamlit as st

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
#url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/historical'
parameters = {

  'start':'1',
  'limit':'5000',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': st.secrets['CM_API'],
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)
for idx in range(len(data['data'])):
  if st.session_state['Token']==data['data'][idx]['symbol']:
    token_index=idx
    st.write(f"Token ID: {token_index}")
    st.write(f"Token Name: {data['data'][token_index]['name']}")
    st.write(f"Token Circulating Supply: {data['data'][token_index]['circulating_supply']:,}")
