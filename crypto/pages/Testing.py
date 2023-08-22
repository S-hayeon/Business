import streamlit as st
from tradingpatterns import tradingpatterns

def main():
    st.title("Head shoulders")
    data=st.session_state["DataFrame"]
    head_shoulder=tradingpatterns.detect_head_shoulder(df=data)
    multiple_top_bottom=tradingpatterns.detect_multiple_tops_bottoms(df=data)
    triangle_pattern=tradingpatterns.detect_triangle_pattern(df=data)
    wedge_pattern=tradingpatterns.detect_wedge(df=data)
    double_topbottom_pattern=tradingpatterns.detect_double_top_bottom(df=data)
    data[['head_shoulder_pattern','multiple_top_bottom_pattern','triangle_pattern','wedge_pattern','double_pattern']]
    #st.write(data.index)
    #st.write(data.columns)
    st.write(data)
    

if __name__ == "__main__":
    main()
