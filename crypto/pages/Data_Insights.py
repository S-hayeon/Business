import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import requests
import scipy
import streamlit as st
import tweepy
box_plot_caption=""
data=st.session_state['DataFrame']
st.title(f"{st.session_state['CoinPair']} Data Insights")
ohlcv=['Open','High','Low','Close','Volume']
data=data[ohlcv]
data_option=st.sidebar.radio("Select Data option",options=ohlcv)
with st.expander("Coin Pair Data"):
  st.dataframe(data)
with st.expander("Descriptive Stats"):
  st.dataframe(data.describe())
  st.header("Measures of Central Tendency")
  stats_DF=pd.DataFrame({'Median': data[data_option].median(),
                     'Standard Deviation': data[data_option].std(),
                     'InterQuartile Range':data[data_option].quantile(0.75)-data[data_option].quantile(0.25)},index=['-'])
  st.dataframe(stats_DF)
def send_telegram_Message():
  bot_token=st.secrets['bot_token']
  chat_id=st.secrets['chat_id']
  url = f'https://api.telegram.org/bot{bot_token}/sendPhoto' # URL to the Telegram Bot API for sending photos
  #caption = f"Coin Pair:{st.session_state['CurrencyPair']}\nStart Date: {st.session_state['Start_Date']} to {st.session_state['End_Date']}\nInterval={st.session_state['Interval']}\nSupport Level: {st.session_state['support']}\nResistance Level: {st.session_state['resistance']}\n{st.session_state['DataFrame'].iloc[-1]}"
  caption = f"Coin Pair:{st.session_state['CurrencyPair']}\nCrypto Token: ${st.session_state['Token']}\nCrypto Token Category:{st.session_state['TokenCategory']}\nStart Date: {st.session_state['Start_Date']} to {st.session_state['End_Date']}\nInterval={st.session_state['Interval']}\nBox Plot for the {data_option} values\n{box_plot_caption}\n#CryptoGuideBotTrading"
  payload = {'chat_id': chat_id,'caption': caption}     
  files = {'photo': open(box_image_file_path, 'rb')} # Prepare the payload
  response = requests.post(url, data=payload, files=files) # Send the photo
  if response.status_code == 200:
    st.toast('Data Insights available!')
    # if os.path.exists(bar_image_file_path):
    #   os.remove(bar_image_file_path)
    if os.path.exists(box_image_file_path):
      os.remove(box_image_file_path)
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
  auth = tweepy.OAuth1UserHandler(apiKey, apiSecret)
  auth.set_access_token(accessToken,accessSecret)
  api = tweepy.API(auth)
  media = api.media_upload(filename=box_image_file_path)
  media_id = media.media_id
  caption = f"Coin Pair:{st.session_state['CurrencyPair']}\nCrypto Token: ${st.session_state['Token']}\nCrypto Token Category:{st.session_state['TokenCategory']}\nStart Date: {st.session_state['Start_Date']} to {st.session_state['End_Date']}\nInterval={st.session_state['Interval']}\nBox Plot for the {data_option} values\n{box_plot_caption}#CryptoTradingGuideBot."
  client.create_tweet(media_ids=[media_id], text=caption)
if st.sidebar.button("View Insights"):
    st.header("Percentiles")
    percentileDF = pd.DataFrame({'Percentiles': data[data_option].quantile([0.05, 0.25, 0.5, 0.75, 0.95])}, index=['-'])
    st.write(percentileDF)
    # stats_DF = pd.DataFrame()
    # # Loop through each OHLCV column and calculate statistics
    # for column in ohlcv:
    #   stats_DF[column + ' Median'] = data[column].median()
    #   stats_DF[column + ' Standard Deviation'] = data[column].std()
    #   stats_DF[column + ' Percentiles'] = data[column].quantile([0.05, 0.25, 0.5, 0.75, 0.95])
    #   stats_DF[column + ' InterQuartile Range'] = data[column].quantile(0.75) - data[column].quantile(0.25)
    # st.dataframe(stats_DF)
    st.header( f"{data_option} Frequency Table")
    binned_data=pd.cut(data[data_option],10)
    value_counts = binned_data.value_counts().reset_index()
    # Rename the columns for clarity
    value_counts.columns = ['Bin Range', 'Count']
    # Format the "Bin Range" column
    value_counts['Bin Range'] = value_counts['Bin Range'].apply(lambda x: f"{x.left:.4f} - {x.right:.4f}" if (x.right - x.left) < 1 else f"{x.left:.2f} - {x.right:.2f}")
    # Print the frequency table
    st.dataframe(value_counts)
    st.header("Box Plot")
    box_plot = data[data_option].plot.box()
    #box_plot.set_xlabel("index")
    box_plot.set_xlabel(f"{st.session_state['Start_Date']} - {st.session_state['End_Date']}")
    box_plot.set_ylabel(f"{st.session_state['CoinPair']} {data_option} values")
    box_image_file_path = f"{st.session_state['CoinPair']}_boxPlot.png"
    plt.savefig(box_image_file_path)
    st.pyplot(box_plot.figure)
    with st.expander("More info on Box Plot"):
      minimum = data[data_option].min()
      st.write(f":green[Minimum: {minimum}]")
      box_plot_caption+=f"Minimum: {minimum}\n"
      maximum = data[data_option].max()
      box_plot_caption+=f"Maximum: {maximum}\n"
      st.write(f":red[Maximum: {maximum}]")
      percentile_75 = np.percentile(data[data_option], 75)
      box_plot_caption+=f"75th Perentile: {percentile_75}\n"
      st.write(f":blue[75th Perentile: {percentile_75}]")
      percentile_25 = np.percentile(data[data_option], 25)
      box_plot_caption+=f"25th Perentile: {percentile_25}\n"
      st.write(f":blue[25th Perentile: {percentile_25}]")
      IQR = round(percentile_75 - percentile_25,4)
      box_plot_caption+=f"Inter Quartile Range: {IQR}\n"
      st.write(f"Inter Quartile Range: {IQR}")
      median = data[data_option].median()
      st.write(f":orange[Median: {median}]")
      box_plot_caption+=f"Median: {median}\n"
    #st.write(box_plot_caption)
    send_twitter_Message()
    send_telegram_Message()

                 
