import streamlit as st
import talib
if __name__=='__main__':
  techanalysis=TIndicators(st.session_state["DataFrame"])
  indicatorsDF=techanalysis.techIndicators()
  st.dataframe(indicatorsDF)
