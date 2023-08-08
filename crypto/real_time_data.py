import streamlit as st
import websocket

info_placeholder = st.empty()
error_placeholder = st.empty()
text_placeholder = st.empty()
SOCKET = "wss://stream.binance.com:443/ws/ethusdt@kline_1m"
ws = None  # Initialize the WebSocket instance

def on_open(ws):
    info_placeholder.info("Nimefungua data stream")

def on_close(ws):
    info_placeholder.info("Nimefunga data stream")

def on_message(ws, message):
    st.info("Data stream sasa inaFlow")
    st.text(message)

st.title("Crypto Live Datastream")

# Create a button to start the WebSocket connection
if st.button("Start Data Stream"):
    def start_stream():
        global ws
        ws = websocket.WebSocketApp(
            SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
        ws.run_forever()
    
    start_stream()
