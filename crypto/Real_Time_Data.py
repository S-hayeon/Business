import streamlit as st
import websocket
import json

# Streamlit configuration
st.set_page_config(page_title="Binance WebSocket App", layout="wide")

# Binance WebSocket endpoint
BINANCE_WS_ENDPOINT = "wss://stream.binance.com:9443/ws/btcusdt@trade"

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
    ws = websocket.WebSocketApp(binance_ws_endpoint, on_message=on_message)
    st.sidebar.write("WebSocket status:", ws.sock.connected)

    if not ws.sock.connected:
        st.sidebar.error("WebSocket connection failed.")
    else:
        ws.run_forever()

