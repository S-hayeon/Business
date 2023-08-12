# Import the necessary libraries
import matplotlib.pyplot as plt
#from mpl_finance import candlestick_ohlc
import mplfinance as mpf
import pandas as pd
#from streamlit import caching
import streamlit as st
import sys
try:
    sys.path.append('/app/business')
    from crypto import main
    from Technical_Analysis import chart_patterns
except:  
    sys.path.append('/mount/src/business')
    from crypto import main
    from Technical_Analysis import chart_patterns
#sys.path.append('/app/business/fx')
import time
st.session_state['SupportResistance_Figure']=None

if st.session_state['CurrencyPair'] is not None and st.session_state['DataFrame'] is not None:
    def support_Resistance():
        status_displayed = False  # Flag to track whether status message has been displayed
        # Continuously update the data by fetching new data from the API
        #lookback=st.slider(label="Sensitivity in Percentage %", min_value=1, max_value=100, value=25, step=1)
        data_placeholder.dataframe(st.session_state['DataFrame'].describe())
        # Display status message only once
        chart_pattern=chart_patterns.Pattern(data=st.session_state['DataFrame'])
        support_resistance_lines=list(chart_pattern.support_resistance())
        #support_resistance_lines=list(chart_pattern.support_resistance(int(lookback)))
        st.session_state['support_resistance_lines'] = support_resistance_lines
        fig=mpf.plot(st.session_state['DataFrame'],type='candle',volume=True,style='binance',hlines=dict(hlines=support_resistance_lines,colors=['g','r'],linestyle='-.'))
        #candlestickfigure_placeholder.pyplot(fig)
        st.pyplot(fig)
        time.sleep(2)  # Wait for 2 seconds
    #st.set_option('deprecation.showPyplotGlobalUse', False)
    with st.container():
        st.title('Chart Patterns :chart:')
        st.header(":green[Support] and :red[Resistance] Levels")
        data_placeholder = st.empty() # Create a placeholder for the dataframe
        candlestickfigure_placeholder = st.empty() # Create a placeholder for the candlestickfigure
        support_Resistance()
    with st.expander("More info on Support and Resistance"):
        #st.info("Sensitivity is the % of data the system looks back to find support and resistance.")
        # Access support_resistance_lines from st.session_state
        support_level = st.session_state.support_resistance_lines[0]
        resistance_level = st.session_state.support_resistance_lines[1]
        #st.markdown(f"**Support Level** is: {support_level}", unsafe_allow_html=True)
        st.markdown(f":green[Support Level] is: {support_level}", unsafe_allow_html=True)
        st.markdown(f":red[Resistance Level] is: {resistance_level}", unsafe_allow_html=True)
        candlestickID=chart_patterns.Pattern(data=st.session_state['DataFrame'])
        st.write(f"The last candlestick is {candlestickID.candlestick_Pattern(len(st.session_state['DataFrame'])-1)[0]}")
        st.write(f"The last candlestick trend pattern is {candlestickID.candlestick_Pattern(len(st.session_state['DataFrame'])-1)[1]}")
        # st.session_state['DataFrame']
        # candlestickDF=pd.DataFrame(columns=['Date', 'Pattern','Trend'])
        # for dfindex in range(len(st.session_state['DataFrame'])):
        #     patternsID=candlestickID.candlestick_Pattern(dfindex)
        #     #candlestickDF.at[dfindex,'Date']=st.session_state['DataFrame'].iloc[dfindex]['Date']
        #     candlestickDF.at[dfindex,'Pattern']=patternsID[0]
        #     candlestickDF.at[dfindex,'Trend']=patternsID[1]
        # candlestickpatterns_placeholder = st.empty() # Create a placeholder for the candlestick Patterns Dataframe 
        # st.write(st.session_state['DataFrame'].columns)
        # with st.expander("View Candlestick Patterns"):
        #     candlestickpatterns_placeholder.dataframe(candlestickDF)
