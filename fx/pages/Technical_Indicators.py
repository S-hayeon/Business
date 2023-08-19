import streamlit as st
import sys
try:
    sys.path.append('/app/business')
    from Technical_Analysis import Technical_indicators
except:  
    sys.path.append('/mount/src/business')
    from Technical_Analysis import Technical_indicators
techanalysis=Technical_indicators.TIndicators(data=st.session_state['DataFrame'])
indicatorsDF=techanalysis.techIndicators()
st.dataframe(indicatorsDF)
