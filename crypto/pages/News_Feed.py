import matplotlib.pyplot as plt
import os
import pandas as pd
import requests
import streamlit as st
from wordcloud import WordCloud
API_KEY=st.secrets['CP_API']
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
url=make_url(currencies=st.session_state['Token'],kind='news',region='en')
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
response=get_page_json(url)['results']
def get_df(data):
    """Return pandas DF."""
    df = pd.DataFrame(data)
    try:
        df['created_at'] = pd.to_datetime(df.created_at)
    except Exception as e:
        pass

    return df
df=get_df(response)
def stripContents(text):
    return text.strip()
title_list=df['title'].apply(stripContents).tolist()
title_paragraph=" ".join(map(str,title_list))
wordcloud=WordCloud(background_color='orange',max_words=1000,width=800,height=400).generate(title_paragraph)
plt.figure(figsize=(10,5))
plt.imshow(wordcloud,interpolation='bilinear')
plt.axis('off')
wordcloudImage=f"{st.session_state['CoinPair']}_wordcloud.png"
plt.savefig(wordcloudImage)  # Save as PNG
st.image(wordcloudImage)
if os.path.exists(wordcloudImage):
      os.remove(wordcloudImage)
