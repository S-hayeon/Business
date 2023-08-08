import streamlit as st
import websocket

info_placeholder = st.empty()
error_placeholder = st.empty()
text_placeholder = st.empty()
SOCKET = "wss://stream.binance.com:443/ws/ethusdt@kline_1m"
ws = None  # Initialize the WebSocket instance

def on_open(ws):
    info_placeholder.info("Nimefungua data stream")

def on_error(ws, error):
    error_placeholder.error(error)

def on_close(ws):
    info_placeholder.info("Nimefunga data stream")

def on_message(ws, message):
    info_placeholder.info("Data stream sasa inaFlow")
    text_placeholder.text(message)

st.title("Crypto Live Datastream")

# Create a button to start the WebSocket connection
if st.button("Start Data Stream"):
    ws = websocket.WebSocketApp(
        SOCKET, on_open=on_open, on_close=on_close, on_message=on_message, on_error=on_error
    )
    ws.run_forever()
