import streamlit as st
import sys
try:
    sys.path.append('/app/business')
    from crypto import main
    from Technical_Analysis import Technical_indicators
except:  
    sys.path.append('/mount/src/business')
    from crypto import main
    from Technical_Analysis import Technical_indicators
technicalIndicators=Technical_indicators.TIndicators(data=st.session_state['DataFrame'])
#macd=technicalIndicators.MACD()
bull_bear=technicalIndicators.BullBearish_state()
st.write("The market trend is: ",bull_bear)
