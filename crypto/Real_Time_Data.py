import streamlit as st
import websocket
import threading
import json

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
binance_ws_endpoint = f"wss://stream.binance.com:9443/ws/{symbol}@trade"

if symbol:
    st.sidebar.write("WebSocket URL:", binance_ws_endpoint)

    def run_ws():
        ws = websocket.WebSocketApp(binance_ws_endpoint, on_message=on_message)
        ws.run_forever()

    connect_button = st.sidebar.button("Connect")
    
    if connect_button:
        thread = threading.Thread(target=run_ws)
        thread.start()
