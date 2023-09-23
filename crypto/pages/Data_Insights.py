import matplotlib.pyplot as plt
import os
import pandas as pd
import requests
import scipy
import streamlit as st
data=st.session_state['DataFrame']
st.title(f"{st.session_state['CoinPair']} Data Insights")
ohlcv=['Open','High','Low','Close','Volume']
data=data[ohlcv]
data_option=st.sidebar.radio("Select Data option",options=ohlcv)
with st.expander("Coin Pair Data"):
  st.dataframe(data)
bar_plot=data.plot.bar()
bar_image_file_path = f"{st.session_state['CoinPair']}_boxPlot.png"
plt.savefig(bar_image_file_path)
st.pyplot(bar_plot.figure)
with st.expander("Descriptive Stats"):
  st.dataframe(data.describe())
  st.header("Measures of Central Tendency")
  stats_DF=pd.DataFrame({'Median': data[data_option].median(),
                     'Standard Deviation': data[data_option].std(),
                     'InterQuartile Range':data[data_option].quantile(0.75)-data[data_option].quantile(0.25)})
  st.dataframe(stats_DF)
  st.header("Percentiles")       
  percentileDF=pd.DataFrame({'Percentiles':data[data_option].quantile([0.05,0.25,0.5,0.75,0.95])})
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
value_counts['Bin Range'] = value_counts['Bin Range'].apply(lambda x: f"{x.left:.1f} - {x.right:.1f}")
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
#st.image(box_image_file_path) # Testing the exported image.
def send_telegram_Message():
  bot_token=st.secrets['bot_token']
  chat_id=st.secrets['chat_id']
  url = f'https://api.telegram.org/bot{bot_token}/sendPhoto' # URL to the Telegram Bot API for sending photos
  #caption = f"Coin Pair:{st.session_state['CurrencyPair']}\nStart Date: {st.session_state['Start_Date']} to {st.session_state['End_Date']}\nInterval={st.session_state['Interval']}\nSupport Level: {st.session_state['support']}\nResistance Level: {st.session_state['resistance']}\n{st.session_state['DataFrame'].iloc[-1]}"
  caption = f"Coin Pair:{st.session_state['CurrencyPair']}\nCrypto Token Category:{st.session_state['TokenCategory']}\nStart Date: {st.session_state['Start_Date']} to {st.session_state['End_Date']}\nInterval={st.session_state['Interval']}\nBox Plot for the {data_option} values\n#CryptoGuideBotTrading"
  payload = {'chat_id': chat_id,'caption': caption}     
  files = {'photo': open(box_image_file_path, 'rb')} # Prepare the payload
  response = requests.post(url, data=payload, files=files) # Send the photo
  if response.status_code == 200:
    st.toast('Data Insights available!')
    if os.path.exists(bar_image_file_path):
      os.remove(bar_image_file_path)
    if os.path.exists(box_image_file_path):
      os.remove(box_image_file_path)
  else:
      #st.toast('Failed to send photo. Status code:', response.status_code)
      st.toast(response.text)
#send_telegram_Message()
                 
