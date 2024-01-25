import datetime
from gnews import GNews
import matplotlib.pyplot as plt
import os
import pandas as pd
import requests
import streamlit as st
import sys
try:
    sys.path.append('/app/business')
    from crypto import main
except:  
    sys.path.append('/mount/src/business')
    from crypto import main
import time
import tweepy
from wordcloud import WordCloud
API_KEY=st.secrets['CP_API']
google_news=GNews()
st.title(f"{st.session_state['CoinPair']} NEWS Feed")
current_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def googleNews(search_symbol):
    titles=[]
    latest_news=google_news.get_news(search_symbol)
    for item in latest_news:
        title=item['title']
        titles.append(title)
    return titles
def make_url(filter=None, currencies=None, kind=None, region=None, page=None):
    """Handle of URL variables for API POST."""
    url = 'https://cryptopanic.com/api/v1/posts/?auth_token={}'.format(API_KEY)

    if currencies is not None:
        if len(currencies.split(',')) <= 50:
            url += "&currencies={}".format(currencies)
        else:
            print("Warning: Max Currencies is 50")
            return

    if kind is not None and kind in ['news', 'media']:
        url += "&kind={}".format(kind)

    filters = ['rising', 'hot', 'bullish', 'bearish', 'important', 'saved', 'lol']
    if filter is not None and filter in filters:
        url += "&filter={}".format(filter)

    regions = ['en', 'de', 'es', 'fr', 'it', 'pt', 'ru']  # (English), (Deutsch), (Español), (Français), (Italiano), (Português), (Русский)--> Respectively
    if region is not None and region in regions:
        url += "&region={}".format(region)

    if page is not None:
        url += "&page={}".format(page)

    return url
newsurl=make_url(currencies=st.session_state['Token'],kind='news',region='en')
multimediaurl=make_url(currencies=st.session_state['Token'],kind='news',region='en')
def get_page_json(url=None):
    """
    Get First Page.

    Returns Json.

    """
    #time.sleep()
    if not url:
        url = "https://cryptopanic.com/api/v1/posts/?auth_token={}".format(API_KEY)
    page = requests.get(url)
    data = page.json()
    return data
multimedia_response=get_page_json(multimediaurl)['results']
news_response=get_page_json(newsurl)['results']
def get_df(data):
    """Return pandas DF."""
    df = pd.DataFrame(data)
    try:
        df['created_at'] = pd.to_datetime(df.created_at)
    except Exception as e:
        pass

    return df
multimedia_df=get_df(multimedia_response)
news_df=get_df(news_response)
def stripContents(text):
    return text.strip()
def send_telegram_Message(type,image_file_path):
    bot_token=st.secrets['bot_token']
    chat_id=st.secrets['chat_id']
    url = f'https://api.telegram.org/bot{bot_token}/sendPhoto' # URL to the Telegram Bot API for sending photos
    #caption = f"Coin Pair:{st.session_state['CurrencyPair']}\nStart Date: {st.session_state['Start_Date']} to {st.session_state['End_Date']}\nInterval={st.session_state['Interval']}\nSupport Level: {st.session_state['support']}\nResistance Level: {st.session_state['resistance']}\n{st.session_state['DataFrame'].iloc[-1]}"
    caption = f"Coin Pair:{st.session_state['CurrencyPair']}\nCrypto Token: ${st.session_state['Token']}\nCrypto Token Category: {st.session_state['TokenCategory']}\n{type} Wordcloud depicting the latest {type} sentiments as of: {current_time}\n#CryptoGuideBotTrading"
    payload = {'chat_id': chat_id,'caption': caption}     
    files = {'photo': open(image_file_path, 'rb')} # Prepare the payload
    response = requests.post(url, data=payload, files=files) # Send the photo
    if response.status_code == 200:
        st.toast('News feed available!')
        if os.path.exists(image_file_path):
            os.remove(image_file_path)
    else:
        #st.toast('Failed to send photo. Status code:', response.status_code)
        st.toast(response.text)
def send_twitter_Message(type,image_file_path):
    apiKey= st.secrets['apiKey']
    apiSecret=st.secrets['apiSecret']
    bearerToken=st.secrets['bearerToken']
    accessToken=st.secrets['accessToken']
    accessSecret=st.secrets['accessSecret']
    client = tweepy.Client(bearer_token=bearerToken,consumer_key=apiKey,consumer_secret=apiSecret,access_token=accessToken,access_token_secret=accessSecret)
    #auth = tweepy.OAuth1UserHandler(apiKey, apiSecret)
    auth = tweepy.OAuthHandler(apiKey, apiSecret)
    auth.set_access_token(accessToken,accessSecret)
    api = tweepy.API(auth)
    media = api.media_upload(filename=image_file_path)
    media_id = media.media_id
    caption = f"Coin Pair:{st.session_state['CurrencyPair']}\nCrypto Token: ${st.session_state['Token']}\nCrypto Token Category: {st.session_state['TokenCategory']}\n{type} Wordcloud depicting the latest {type} sentiments as of: {current_time}\n#CryptoTradingGuideBot"
    client.create_tweet(media_ids=[media_id], text=caption)
multimedia_title_list=multimedia_df['title'].apply(stripContents).tolist()
news_title_list=news_df['title'].apply(stripContents).tolist()
multimedia_paragraph=" ".join(map(str,multimedia_title_list))
news_paragraph=" ".join(map(str,news_title_list))
st.toast("Retrieved news from Crypto articles")
time.sleep(2)
search_symbol=main.crypto_dict[st.session_state['Token']]
google_news=googleNews(search_symbol)
news_paragraph = " ".join(set(map(str, google_news)))
st.toast("Combined news from Google articles")
time.sleep(2)
multimedia_wordcloud=WordCloud(background_color='white',max_words=3000).generate(multimedia_paragraph)
fig, ax = plt.subplots() 
ax.imshow(multimedia_wordcloud, interpolation='bilinear') 
ax.axis("off") 
media_wordcloud_img=f"{st.session_state['CoinPair']}_media_wordcloud.png"
# send_telegram_Message(type="Youtube Media",image_file_path=media_wordcloud_img)
# send_twitter_Message(type="Youtube Media",image_file_path=media_wordcloud_img)
#plt.savefig(media_wordcloud_img)  # Save as PNG
plt.savefig(media_wordcloud_img, transparent=True, bbox_inches='tight', pad_inches=0)
st.header("Latest :red[Youtube] Sentiments")
st.pyplot(fig)
#st.image(media_wordcloud_img)
if os.path.exists(media_wordcloud_img):
      os.remove(media_wordcloud_img)
news_wordcloud=WordCloud(background_color='white',max_words=3000).generate(news_paragraph)
fig, ax = plt.subplots() 
ax.imshow(news_wordcloud, interpolation='bilinear') 
ax.axis("off") 
news_wordcloud_img=f"{st.session_state['CoinPair']}_news_wordcloud.png"
plt.savefig(news_wordcloud_img)  # Save as PNG
plt.savefig(news_wordcloud_img, transparent=True, bbox_inches='tight', pad_inches=0)
st.header("Latest :blue[News] Sentiments")
st.pyplot(fig)
send_twitter_Message(type="News",image_file_path=news_wordcloud_img)
send_telegram_Message(type="News",image_file_path=news_wordcloud_img)
#st.image(news_wordcloud_img)
if os.path.exists(news_wordcloud_img):
      os.remove(news_wordcloud_img)
