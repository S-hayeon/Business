#Import the necessary libraries 
import ccxt
import dataframe_image as dfi
from datetime import datetime, timedelta
#import datetime
from io import BytesIO
import matplotlib.pyplot as plt
#from mpl_finance import candlestick_ohlc
import mplfinance as mpf
import numpy as np
import os
import pandas as pd
import requests
#from streamlit import caching
import streamlit as st
import sys
try:
    sys.path.append('/app/business')
    from crypto import main
except:  
    sys.path.append('/mount/src/business')
    from crypto import main
#sys.path.append('/app/business/fx')
import talib
import time
import zipfile
refresh_interval=60 # Refresh in 60 seconds
st.session_state['CoinPair']=None
st.session_state['DataFrame']=None
st.session_state['End_Date']=None
st.session_state['Start_Date']=None
cryptolist = ['BTCBUSD', 'BTCUSDT', 'ETHBUSD', 'ETHUSDT', 'BNBUSDT', 'BNBBUSD', 'XRPBUSD', 'XRPUSDT','ADABUSD', 'ADAUSDT', 'MATICBUSD', 'MATICUSDT', 'SHIBBUSD', 'SHIBUSDT', 'DOGEBUSD', 'DOGEUSDT']
def format_key(key):
    # Split the key by underscores, capitalize each word, and join them with a space
    return " ".join(word.capitalize() for word in key.split('_'))
def coin_token_selection():
    # Coin, Token dictionary containing the keys and values for the dropdowns
    # First dropdown for selecting the Token key
    token_selected_key = st.sidebar.selectbox("Select your Token Category:", list(sorted(main.crypto_tokens.keys())))
    token_selected_value = st.sidebar.selectbox("Select a Token currency:", sorted(main.crypto_tokens[token_selected_key]))
    if token_selected_value in main.crypto_dict and main.crypto_dict[token_selected_value] != "-":
        st.session_state['TokenName'] = main.crypto_dict[token_selected_value]
    else:
        st.session_state['TokenName'] =""
    coin_selected_key = st.sidebar.selectbox("Select your Coin Currency:", [format_key(key) for key in main.crypto_coins.keys()])
    # Convert the formatted key back to the original key with underscores
    coin_original_key = "_".join(word.lower() for word in coin_selected_key.split())
    # Second dropdown showing values based on the selected key
    coin_selected_value = st.sidebar.selectbox("Select your Coin Currency Symbol:", main.crypto_coins[coin_original_key])
    st.session_state['Token']= token_selected_value
    #st.session_state['TokenName']= main.crypto_dict[token_selected_value]
    st.session_state['TokenCategory']= token_selected_key
    st.session_state['CoinPair']= f"{token_selected_value}{coin_selected_value}"
    st.sidebar.success(f"Coin pair is: {st.session_state['CoinPair']} ",icon="✅")
#@st.cache_data(ttl=3600)
#     url = f"https://api.binance.com/api/v3/klines"
def format_url(symbol, type, interval, date):
    if type == 'Daily':
        base_url = 'https://data.binance.vision/data/spot/daily/klines/'
    elif type == 'Monthly':
        base_url = 'https://data.binance.vision/data/spot/monthly/klines/'
    else:
        return None

    url_formatted = f"{base_url}{symbol}/{interval}/{symbol}-{interval}-{date}.zip"
    return url_formatted

# Function to download and extract data
def download_and_extract_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        with zipfile.ZipFile(BytesIO(response.content), 'r') as zip_file:
            file_list = zip_file.namelist()
            if len(file_list) == 1:
                with zip_file.open(file_list[0]) as csv_file:
                    datatable = pd.read_csv(csv_file)
                    datatable = datatable.iloc[:, :6]  # All rows and columns up to 6
                    datatable.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
                    datatable = datatable.set_index('Date')  # Note this is in ms
                    datatable.index = pd.to_datetime(datatable.index, unit='ms')
                    datatable = datatable.astype(float)  # Convert values from strings to float
                return datatable
            else:
                print("Error: The .zip file contains more than one file.")
    else:
        print(f"Error: Failed to download the .zip file from {url}")
@st.cache_resource(show_spinner=True)
# Function to retrieve historical data for a date range
def get_historical_data(symbol, type, interval, start_date, end_date):
    combined_data = pd.DataFrame()
    current_date = start_date

    while current_date <= end_date:
        formatted_date = current_date.strftime('%Y-%m-%d')
        url = format_url(symbol, type, interval, formatted_date)
        
        if url:
            data = download_and_extract_data(url)
            if data is not None:
                combined_data = pd.concat([combined_data, data])
        
        current_date += timedelta(days=1)

    return combined_data
def round_value(input_value):
    if input_value>1:
        a=round(input_value,3) # Round values above 1 to 3 decimal
    else:
        a=round(input_value,8) # Round values less than 1 to 8 decimal places
    return a
def recent_tech_indicators(interval):
    # Initialize a dictionary to store DataFrames for each cryptocurrency
    crypto_data = {}
    start_date = datetime.now() - timedelta(days=3)  # Last 3 days
    end_date = datetime.now()
    # Iterate through the list of cryptocurrencies and retrieve recent data
    for symbol in cryptolist:
        data = get_historical_data(symbol,'Daily',interval,start_date, end_date)
        if data is not None:
            # Extract relevant data for ADX and RSI calculation
            high = data['High']
            low = data['Low']
            close = data['Close']
            # Calculate ADX
            adx = talib.ADX(high, low, close, timeperiod=14)
            # Calculate RSI
            rsi = talib.RSI(close, timeperiod=14)
            # Create a DataFrame for the current symbol pair
            crypto_df = pd.DataFrame({
                'Date': data.index,
                'ADX': adx,
                'RSI': rsi
            })
            # Store the DataFrame in the dictionary with the symbol as the key
            crypto_data[symbol] = crypto_df
    for symbol in cryptolist:
        coin_data = crypto_data[symbol]
        last_adx_value = coin_data['ADX'][len(coin_data)-1]
        prev_adx_value = coin_data['ADX'][len(coin_data)-2]
        if not np.isnan(last_adx_value) and not np.isnan(prev_adx_value) and last_adx_value != 0:
            adx_change=((last_adx_value-prev_adx_value)/last_adx_value)*100
        else:
            adx_change=0
        last_rsi_value = coin_data['RSI'][len(coin_data)-1]
        prev_rsi_value = coin_data['RSI'][len(coin_data)-2]
        if not np.isnan(last_rsi_value) and not np.isnan(prev_rsi_value) and last_rsi_value != 0:
            rsi_change=((last_rsi_value-prev_rsi_value)/last_rsi_value)*100
        else:
            rsi_change=0
        #st.write(f'## {coin_pair} Analysis')
        # Display coin symbol and ADX and RSI values using st.metric()
        col1, col2, col3 = st.columns(3)
        # Set the width of col1 to be wider
        col1_width = 1200  # You can adjust this value
        # Create custom CSS styles to control the column widths
        col1_style = f"width: {col1_width}px;"
        col2_style = "width: auto;"
        col3_style = "width: auto;"
        # Apply the custom styles to the columns
        col1.markdown(f'<div style="{col1_style}"></div>', unsafe_allow_html=True)
        col2.markdown(f'<div style="{col2_style}"></div>', unsafe_allow_html=True)
        col3.markdown(f'<div style="{col3_style}"></div>', unsafe_allow_html=True)
        with col1:
            st.metric("Coin Pair", symbol)
        with col2:
            st.metric("ADX",round(last_adx_value, 2),f"{round(adx_change, 2)}%")
        with col3:
            st.metric("RSI",round(last_rsi_value,2),f"{round(rsi_change,2)}%")
def peakTroughPlot(data,cointitle):
    # Define short-term and long-term periods
    short_period = 5
    long_period = 20
    """# Calculate moving averages
    data['SMA_short'] = data['Close'].rolling(window=short_period).mean()
    data['SMA_long'] = data['Close'].rolling(window=long_period).mean()
    #  "Peak" is defined as a price where the current closing price is greater than both the previous and next closing prices.
    data['Peak'] = data['Close'][(data['Close'] > data['Close'].shift(1)) & (data['Close'] > data['Close'].shift(-1))]
    # A "Trough" is defined as a price where the current closing price is less than both the previous and next closing prices.
    data['Trough'] = data['Close'][(data['Close'] < data['Close'].shift(1)) & (data['Close'] < data['Close'].shift(-1))]
    # Create a dictionary to specify legend labels for your features
    legend_dict = {
    'SMA_short': 'Short SMA',
    'SMA_long': 'Long SMA',
    'Peak': 'Peaks',
    'Trough': 'Troughs'}
    sma_short=data['SMA_short']
    sma_long=data['SMA_long']
    # Create addplots with legend labels
    feature_plots = [
    mpf.make_addplot(sma_short, label=legend_dict['SMA_short']),
    mpf.make_addplot(sma_long, label=legend_dict['SMA_long']),
    mpf.make_addplot(data['Peak'], type='scatter', color='r', markersize=100, marker='^', label=legend_dict['Peak']),
    mpf.make_addplot(data['Trough'], type='scatter', color='k', markersize=100, marker='v', label=legend_dict['Trough']),
]
    with st.expander(f"{cointitle} Peaks and Troughs Plot"):
        # Create the plot
        fig, ax = plt.subplots()
        mpf.plot(data, type='candle', style='binance', title=f"{cointitle} Peaks and Troughs Plot", addplot=feature_plots, figscale=1.25, volume=True, ax=ax)
        st.header(f":blue[{cointitle} Peaks and Troughs Plot]")
        peakTrough_fig.pyplot(fig)
        peak_troughDF = data.loc[data['Peak'].notna() | data['Trough'].notna(), ['Peak', 'Trough']]
        st.header(f":blue[{cointitle} Peaks and Troughs Table]")
        st.dataframe(peak_troughDF)"""
def popularCoinPrices():
    start_date = datetime.now() - timedelta(days=2)  # Last 3 days
    end_date = datetime.now()
    interval='1d'
    col1,col2,col3 =st.columns(3)
    for index, symbol in enumerate(cryptolist):
        popularcoinDF = get_historical_data(symbol,'Daily',interval,start_date, end_date)
        crypto_df = popularcoinDF[popularcoinDF.symbol == symbol]
        crypto_price = round_value(float(crypto_df.weightedAvgPrice.iloc[0]))
        crypto_percent = '{:.2f}%'.format(float(crypto_df.priceChangePercent.iloc[0]))
        #print("{} {} {}".format(symbol, crypto_price, crypto_percent))
        if index % 3 == 0:
            col=col1
        elif index%3==1:
            col=col2
        else:
            col=col3
        with col:
            st.metric(symbol,crypto_price, crypto_percent)
def send_telegram_Message(image_file_path):
    bot_token=st.secrets['bot_token']
    chat_id=st.secrets['chat_id']
    url = f'https://api.telegram.org/bot{bot_token}/sendPhoto' # URL to the Telegram Bot API for sending photos
    #caption = f"Coin Pair:{st.session_state['CurrencyPair']}\nStart Date: {st.session_state['Start_Date']} to {st.session_state['End_Date']}\nInterval={st.session_state['Interval']}\nSupport Level: {st.session_state['support']}\nResistance Level: {st.session_state['resistance']}\n{st.session_state['DataFrame'].iloc[-1]}"
    caption = f"Coin Pair: {st.session_state['CurrencyPair']}\nTrading Session Total volume\nStart Date: {st.session_state['Start_Date']} to {st.session_state['End_Date']}\nnInterval={st.session_state['Interval']} \n#CryptoGuideBotTrading"
    payload = {'chat_id': chat_id,'caption': caption}     
    files = {'photo': open(image_file_path, 'rb')} # Prepare the payload
    response = requests.post(url, data=payload, files=files) # Send the photo
    if response.status_code == 200:
        st.toast('Chart Patterns available!')
        #if os.path.exists(image_file_path):
            #os.remove(image_file_path)
    else:
        #st.toast('Failed to send photo. Status code:', response.status_code)
        st.toast(response.text)
def send_twitter_Message(image_file_path):
    apiKey= st.secrets['apiKey']
    apiSecret=st.secrets['apiSecret']
    bearerToken=st.secrets['bearerToken']
    accessToken=st.secrets['accessToken']
    accessSecret=st.secrets['accessSecret']
    client = tweepy.Client(bearer_token=bearerToken,consumer_key=apiKey,consumer_secret=apiSecret,access_token=accessToken,access_token_secret=accessSecret)
    auth = tweepy.OAuthHandler(apiKey, apiSecret)
    auth.set_access_token(accessToken,accessSecret)
    api = tweepy.API(auth)
    media = api.media_upload(filename=image_file_path)
    media_id = media.media_id
    caption = f"Coin Pair: {st.session_state['CurrencyPair']}\nCrypto Token: ${st.session_state['Token']}\nCrypto Token Category: {st.session_state['TokenCategory']}\nStart Date: {st.session_state['Start_Date']} to {st.session_state['End_Date']}\nInterval={st.session_state['Interval']}\nSupport Level: {st.session_state['support']}\nResistance Level: {st.session_state['resistance']}\n#CryptoTradingGuideBot."
    client.create_tweet(media_ids=[media_id], text=caption)
def trading_session(time):
    hour = time.hour
    sessions = []
    if (hour >= 23 or hour <= 8):
        sessions.append('Sydney')
    if (hour >= 0 and hour <= 9):
        sessions.append('Tokyo')
    if (hour >= 8 and hour <= 16):
        sessions.append('London')
    if (hour >= 13 and hour <= 22):
        sessions.append('New York')
    return ', '.join(sessions) if sessions else 'Closed'

def visualize_data(df,title_text):
    # Continuously update the data by fetching new data from the API
    #while True:
    #df = get_historical_data(st.session_state['CoinPair'], st.session_state['Interval'], st.session_state['Start_Time'],st.session_state['End_Time'])
    # If data is not empty, show the data in the frontend
    if df is not None:
        #st.session_state['DataFrame']=df
        image_file_path = f"{st.session_state['CurrencyPair']}_chart.png"
        title_placeholder.header(f"{st.session_state['CurrencyPair']} Crypto Analysis")
        #fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]}, sharex=True)
        #fig,(ax1, ax2)=plt.subplots()
        #mpf.plot(df, type='candle', volume=True,ax=ax1,volume_ax=ax2,style='binance',savefig=image_file_path,returnfig=True)
        fig, ax = mpf.plot(df, type='candle', volume=True, style='binance', returnfig=True)
        candlestickfigure_placeholder.pyplot(fig)
        #st.image(image_file_path)
        with df_expander_placeholder.expander(f"View the {title_text} data"):
            #data_placeholder.dataframe(df)
            st.dataframe(df)
        # Display the dataframe inside the placeholder
        with expander_placeholder.expander(f"{title_text} Data Statistics"):
            st.markdown(f":blue[The descriptive statistics of OHLCV values:]")
            st.table(df.describe())
def expand_sessions(row):
    sessions = row['Session'].split(', ')
    return [(session, row['Volume']) for session in sessions]	
if __name__=='__main__':
    with st.container():
        #popularCoinPrices()
        #time.sleep(3)
        coin_token_selection()
        st.title(f" :blue[{st.session_state['TokenName']}] Crypto Analysis App")
        #intervals = ['1m', '5m', '15m', '30m', '1h', '4h', '1d','3d','1w','1mo']
        intervals = ['1m', '5m', '15m', '30m', '1h', '4h', '1d']
        interval = st.sidebar.selectbox("Select an interval", intervals)
        st.session_state["Start_Date"] = st.sidebar.date_input("Select the start date:")
        st.session_state["End_Date"] = st.sidebar.date_input("Select the end date:")
        # Create  placeholders
        candlestickfigure_placeholder = st.empty()
        #data_placeholder = st.empty()
        title_placeholder=st.empty()
        df_expander_placeholder = st.empty()
        expander_placeholder = st.empty()

        if st.session_state["Start_Date"] is not None and st.session_state["End_Date"] is not None:
            # Convert start_date and end_date to datetime.datetime objects
            start_datetime = datetime.combine(st.session_state["Start_Date"], datetime.min.time())
            end_datetime = datetime.combine(st.session_state["End_Date"], datetime.min.time()) + timedelta(days=1) - timedelta(milliseconds=1)
            start_time = int(start_datetime.timestamp() * 1000)  # Convert to milliseconds
            #start_time_formatted = datetime.datetime.fromtimestamp(start_time / 1000.0).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            end_time = int(end_datetime.timestamp() * 1000)  # Convert to milliseconds
            #end_time_formatted = datetime.datetime.fromtimestamp(end_time / 1000.0).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            st.session_state['Start_Time']=start_time
            st.session_state['End_Time']=end_time
        if st.sidebar.button('Start Analysis'):
            st.cache_data.clear()
            st.session_state['CurrencyPair']=st.session_state['CoinPair']
            st.session_state['Interval']=interval
            #st.session_state['Start_Time']=start_time
            #st.session_state['End_Time']=end_time
            if st.session_state['CurrencyPair'] is not None:
                @st.cache_resource()
                def get_cached_data(coin_pair, interval, start_date, end_date):
                    #return get_historical_data(symbol=st.session_state['CurrencyPair'], interval=st.session_state['Interval'], start_time=st.session_state['Start_Time'], end_time=st.session_state['End_Time'])
                    return get_historical_data(coin_pair, 'Daily', interval, start_date, end_date)
                # Call the cached function
    
                # Convert the datetime.date object to a string
                start_date_str = st.session_state['Start_Date'].strftime('%Y-%m-%d')
                # Parse the string into a datetime.datetime object
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                end_date_str = st.session_state['End_Date'].strftime('%Y-%m-%d')
                # Parse the string into a datetime.datetime object
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                #df=get_historical_data(symbol=st.session_state['CurrencyPair'], interval=st.session_state['Interval'], start_time=st.session_state['Start_Time'], end_time=st.session_state['End_Time'])
                df = get_cached_data(st.session_state['CoinPair'], st.session_state['Interval'], start_date,end_date)
                #df = get_historical_data(st.session_state['CoinPair'],'Daily',st.session_state['Interval'], st.session_state['Start_Date'],st.session_state['End_Date']).returnDF()
                st.toast("Successful Data Refresh",icon='😍')
                visualize_data(df,st.session_state['CurrencyPair'])
                st.toast("Bar Chart Visualization complete")
                st.session_state['DataFrame']=df
                with st.expander(f"{st.session_state['CoinPair']} Trading Sessions"):
                    df['Session'] = df.index.map(trading_session)
                    st.write('Active Hours for each session:')
                    st.write('Sydney: from 11 PM to 8 AM UTC')
                    st.write('\nNairobi: from 6 AM to 3 PM UTC')
                    st.write('Tokyo: from midnight to 9 AM UTC')
                    st.write('\nLondon: from 8 AM to 4 PM UTC')
                    st.write('New York: from 1 PM to 10 PM UTC')
                    st.dataframe(df[['Open','Close','Volume','Session']]) # Display particular columns
                    expanded_data = [entry for _, row in df.iterrows() for entry in expand_sessions(row)]
                    session_volume_df = pd.DataFrame(expanded_data, columns=['Session', 'Volume'])
                    # Sum the volumes for each session
                    total_volume_by_session = session_volume_df.groupby('Session').sum()
                    #sort in descending order
                    total_volume_by_session=total_volume_by_session.sort_values(by='Volume', ascending=False) #Calculate sum and arrange in Descending order
                    session_df_img=f"{st.session_state['CurrencyPair']}_session_df_img.png"
                    dfi.export(total_volume_by_session,f"{session_df_img}",table_conversion='chrome')
                    send_telegram_Message(image_file_path=session_df_img)
                    st.dataframe(total_volume_by_session)
                    #peakTroughPlot(df,st.session_state['CurrencyPair'])
                    #st.toast("Peak Trough Visualization complete")
            else:
                st.error("Choose a Coin")
        if st.sidebar.button("Start Technical Analysis"):
           with st.expander("Indicators Change in %"):
              recent_tech_indicators(interval)
