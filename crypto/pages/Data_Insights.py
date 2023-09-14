import streamlit as st
data=st.session_state['DataFrame']
with st.expander("Coin Pair Data"):
  st.dataframe(data)
with st.expander("Descriptive Stats"):
  st.dataframe(data.describe())
  st.write(f'Median: {data.median()}')
  st.write(f'Std Deviation: {data.median()}')
  st.write(f'IQR:{data.median()}')
st.header("Box Plot")
box_plot=data['Close'].plot.box()
box_plot.set_xlabel("index")
box_plot.set_ylabel(f"{st.session_state['CoinPair']} Close values")
st.pyplot(box_plot)
        
                 
