import json
import streamlit as st
import websocket

# Streamlit configuration
st.set_page_config(page_title="Binance WebSocket App", layout="wide")

# Initialize Streamlit components
st.title("Binance WebSocket App")
trade_data = st.empty()

# WebSocket callback function
def on_message(ws, message):
    data = json.loads(message)
    trade_data.text(f"Price: {data['p']} | Quantity: {data['q']}")

# Streamlit UI
st.sidebar.header("Settings")
symbol = st.sidebar.text_input("Enter Symbol (e.g., btcusdt)", "btcusdt")
binance_ws_endpoint = f"wss://stream.binance.com:9443/ws/{symbol}@kline_1s"

if symbol:
    st.sidebar.write("WebSocket URL:", binance_ws_endpoint)
    ws = websocket.WebSocketApp(binance_ws_endpoint, on_message=on_message)

    def run_ws():
        ws.run_forever()

    st.sidebar.button("Connect", on_click=run_ws)
