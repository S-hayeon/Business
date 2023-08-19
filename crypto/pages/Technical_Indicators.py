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
# technicalIndicators=Technical_indicators.TIndicators(data=st.session_state['DataFrame'])
# #macd=technicalIndicators.MACD()
# bull_bear=technicalIndicators.BullBearish_state()
# st.write("The market trend is: ",bull_bear)
techanalysis=Technical_indicators.TIndicators(data=st.session_state['DataFrame'])
indicatorsDF=techanalysis.techIndicators()
indicatorsDescribe_placeholder=st.empty()
with indicatorsDescribe_placeholder.expander("Basic Technical Indicators Data"):
    st.dataframe(indicatorsDF.describe())
indicatorsDF_placeholder=st.empty()
with indicatorsDF_placeholder.expander(" Advanced Technical Indicators Data"):
    st.dataframe(indicatorsDF)
