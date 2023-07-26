# Import the necessary libraries
import matplotlib.pyplot as plt
#from mpl_finance import candlestick_ohlc
import mplfinance as mpf
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

try:
    if st.session_state['CurrencyPair'] is not None and st.session_state['DataFrame'] is not None:
        def support_Resistance():
            # Create a placeholder for the dataframe
            data_placeholder = st.empty()
            candlestickfigure_placeholder = st.empty()
            status_displayed = False  # Flag to track whether status message has been displayed
            # Continuously update the data by fetching new data from the API
            while True:
                data_placeholder.dataframe(st.session_state['DataFrame'])
                # Display status message only once
                chart_pattern=chart_patterns.Pattern(data=st.session_state['DataFrame'])
                support_resistance_lines=list(chart_pattern.support_resistance())
                fig=mpf.plot(df,type='candle',volume=True,style='binance',hlines=dict(hlines=support_resistance_lines,colors=['g','r'],linestyle='-.'))
                candlestickfigure_placeholder.pyplot(fig)
        support_Resistance()
        st.set_option('deprecation.showPyplotGlobalUse', False)
    else:
        st.warning("Choose your desired coin from the CryptoAnalysis page to proceed!!")
except Exception as e:
    st.info(f"System encountered {e}")

