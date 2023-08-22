import streamlit as st
from tradingpatterns import tradingpatterns

def main():
    st.title("Head shoulders")
    head_shoulder=tradingpatterns.detect_head_shoulder(df=st.session_state["DataFrame"])
    multiple_top_bottom=tradingpatterns.detect_multiple_tops_bottoms(df=st.session_state["DataFrame"])
    triangle_pattern=tradingpatterns.detect_triangle_pattern(df=st.session_state["DataFrame"])
    wedge_pattern=tradingpatterns.detect_wedge(df=st.session_state["DataFrame"])
    double_topbottom_pattern=tradingpatterns.detect_double_top_bottom(df=st.session_state["DataFrame"])
    #head_shoulder[['head_shoulder_pattern']]
    #st.write(st.session_state["DataFrame"].index)
    #st.write(st.session_state["DataFrame"].columns)
    st.write(st.session_state["DataFrame"])
    

if __name__ == "__main__":
    main()
