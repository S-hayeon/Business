from bs4 import BeautifulSoup
import random
import re
import requests
import streamlit as st
import tweepy
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
link='https://asiliventures.com/index.php/2023/12/03/crypto-dictionary-glossary/'
response = requests.get(link)
html_content = response.content
soup = BeautifulSoup(html_content, 'html.parser')
all_list=soup.find_all("li")
first_item=8
count=86
glossary=all_list[first_item:first_item+count]
random_index=random.randint(0,count-1)
tip=str(glossary[random_index])
# Use a regular expression to remove HTML tags
today_tip = re.sub(r'<.*?>', '',tip)
today_tip_caption=f"Trading 📊Tip💡:{today_tip}"
def send_telegram_Message():
  bot_token=st.secrets['bot_token']
  chat_id=st.secrets['chat_id']
  url = f'https://api.telegram.org/bot{bot_token}/sendMessage' # URL to the Telegram Bot API for sending photos
  #caption = f"Coin Pair:{st.session_state['CurrencyPair']}\nStart Date: {st.session_state['Start_Date']} to {st.session_state['End_Date']}\nInterval={st.session_state['Interval']}\nSupport Level: {st.session_state['support']}\nResistance Level: {st.session_state['resistance']}\n{st.session_state['DataFrame'].iloc[-1]}"
  payload = {'chat_id': chat_id,'text': today_tip_caption}     
  response = requests.post(url, data=payload) # Send the Message
  if response.status_code == 200:
    st.toast('Tokenomics available!')
  else:
    #st.toast('Failed to send photo. Status code:', response.status_code)
    st.toast(response.text)
def send_twitter_Message():
  apiKey= st.secrets['apiKey']
  apiSecret=st.secrets['apiSecret']
  bearerToken=st.secrets['bearerToken']
  accessToken=st.secrets['accessToken']
  accessSecret=st.secrets['accessSecret']
  client = tweepy.Client(bearer_token=bearerToken,consumer_key=apiKey,consumer_secret=apiSecret,access_token=accessToken,access_token_secret=accessSecret)
  auth = tweepy.OAuthHandler(apiKey, apiSecret)
  auth.set_access_token(accessToken,accessSecret) 
  client.create_tweet(text=today_tip_caption)
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
      send_twitter_Message()
      send_telegram_Message()
except:
  st.toast("Coin Pair Tokenomics not available")

