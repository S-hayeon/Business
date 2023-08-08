import streamlit as st
import websocket
info_placeholder=st.empty()
error_placeholder=st.empty()
text_placeholder=st.empty()
SOCKET = "wss://stream.binance.com:443/ws/ethusdt@kline_1m"
def on_open(ws):
  st.info("Nimefungua data stream")
def on_close(ws):
  st.error("Nimefunga data stream")
def on_message(ws,message):
  st.info("Data stream inaFlow")
  print(f"Kuna hii data:{message}")

st.info("Running the Crypto Data stream")
ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever() #Loop the streaming functionality
