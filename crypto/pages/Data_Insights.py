import pandas as pd
import scipy
import streamlit as st
data=st.session_state['DataFrame']
st.title(f"{st.session_state['CoinPair']} Data Insights")
ohlcv=['Open','High','Low','Close','Volume']
data_option=st.sidebar.radio("Select Data option",options=ohlcv)
with st.expander("Coin Pair Data"):
  st.dataframe(data)
with st.expander("Descriptive Stats"):
  st.dataframe(data.describe())
  
  stats_DF=pd.DataFrame({'Median': data[data_option].median(),
                     'Standard Deviation': data[data_option].std(),
                      'Percentiles':data[data_option].quantile([0.05,0.25,0.5,0.75,0.95]),
                     'InterQuartile Range':data[data_option].quantile(0.75)-data[data_option].quantile(0.25)})
  st.dataframe(stats_DF)
  # stats_DF = pd.DataFrame()
  # # Loop through each OHLCV column and calculate statistics
  # for column in ohlcv:
  #   stats_DF[column + ' Median'] = data[column].median()
  #   stats_DF[column + ' Standard Deviation'] = data[column].std()
  #   stats_DF[column + ' Percentiles'] = data[column].quantile([0.05, 0.25, 0.5, 0.75, 0.95])
  #   stats_DF[column + ' InterQuartile Range'] = data[column].quantile(0.75) - data[column].quantile(0.25)
  # st.dataframe(stats_DF)
st.header( f"{data_option} Frequency Table")
binned_data=pd.cut(data[data_option],10)
st.dataframe(binned_data.value_counts())
st.header("Box Plot")
box_plot = data[data_option].plot.box()
#box_plot.set_xlabel("index")
box_plot.set_ylabel(f"{st.session_state['CoinPair']} {data_option} values")
st.pyplot(box_plot.figure)
st.header(f"{st.session_state['CoinPair']} {data_option} Histogram Plot")
histogram=data[data_option].plot.hist()
histogram.set_xlabel(f"{data_option} Data")
histogram.set_ylabel("Frequency")
st.pyplot(histogram.figure)
st.header(f"{st.session_state['CoinPair']} {data_option} Density Plot")
density_plot=data[data_option].plot.kde()
#density_plot.set_x_label(f"{data_option} Density Plot")
st.pyplot(density_plot.figure)
                 
