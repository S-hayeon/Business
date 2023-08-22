import streamlit as st
from tradingpatterns.tradingpatterns import detect_head_shoulder

def main():
    st.title("Head shoulders")
    head_shoulder=detect_head_shoulder(df=st.session_state["DataFrame"])
    head_shoulder[['head_shoulder_pattern']]
    st.write(st.session_state["DataFrame"].index)
    st.write(st.session_state["DataFrame"].columns)
    st.write(head_shoulder)
    

if __name__ == "__main__":
    main()
