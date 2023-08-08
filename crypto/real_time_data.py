import streamlit as st
import websocket
text_placeholder=st.empty()
SOCKET="wss://stream.binance.com:9443/ethusdt@kline_1m"
def on_open(ws):
  text_placeholder.info("Nimefungua data stream")
def on_close(ws):
  text_placeholder.error("Nimefunga data stream")
def on_message(ws,message):
  text_placeholder.info("Data stream inaFlow")
  text_placeholder.write(f"Kuna hii data:{message}")

ws=websocket.WebSocketApp(SOCKET,on_open=on_open,on_close=on_close,on_message=on_message)
ws.run_forever() #Loop the streaming functionality
