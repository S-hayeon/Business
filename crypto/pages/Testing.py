import streamlit as st
from streamlit.components.v1 import html
import pandas as pd
from ipyvizzu import Chart, Data, Config, Style

st.title('🎈 ipyvizzu')

def create_chart():

    # initialize chart
    chart = Chart(width="640px", height="360px", display="manual")

    # add data
    data = Data()
    #data_frame = pd.read_csv("https://github.com/vizzuhq/ipyvizzu/raw/main/docs/examples/stories/titanic/titanic.csv")
    data_frame = st.session_state['DataFrame']
    data.add_data_frame(data_frame)

    chart.animate(data)

    # add config
    chart.animate(Config({"x": "Date", "y": "Open", "label": "Date","title":"Open Prices"}))
    chart.animate(Config({"x": ["Date","Close"], "label": ["Date","Close"], "color": "Close"}))
    chart.animate(Config({"x": "Date", "y": ["High","Low"]}))

    # add style
    chart.animate(Style({"OHLCV data simulation": {"fontSize": 35}}))

    return chart._repr_html_()


CHART = create_chart()
html(CHART, width=650, height=370)
