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


if st.session_state['CurrencyPair'] is not None and st.session_state['DataFrame'] is not None:
    def support_Resistance():
        # Create a placeholder for the dataframe
        data_placeholder = st.empty()
        candlestickfigure_placeholder = st.empty()
        status_displayed = False  # Flag to track whether status message has been displayed
        # Continuously update the data by fetching new data from the API
        lookback=st.slider(label="Sensitivity in Percentage %", min_value=1, max_value=100, value=15, step=1)
        while True:
            data_placeholder.dataframe(st.session_state['DataFrame'])
            # Display status message only once
            chart_pattern=chart_patterns.Pattern(data=st.session_state['DataFrame'])
            support_resistance_lines=list(chart_pattern.support_resistance(int(lookback)))
            fig=mpf.plot(st.session_state['DataFrame'],type='candle',volume=True,style='binance',hlines=dict(hlines=support_resistance_lines,colors=['g','r'],linestyle='-.'))
            candlestickfigure_placeholder.pyplot(fig)
        with st.expander("More info"):
            st.info("Sensitivity is the % of data the system looks back to find support and resistance.")
            st.write(f"Support Level in Green: {support_resistance_lines[0]}")
            st.write(f"Resistance Level in Red: {support_resistance_lines[1]}")
                         
    st.header(":green[Support] and red[Resistance] Levels")
    support_Resistance()
    st.set_option('deprecation.showPyplotGlobalUse', False)
else:
    st.warning("Choose your desired coin from the CryptoAnalysis page to proceed!!")


