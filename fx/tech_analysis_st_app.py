import streamlit as st
import sys
#sys.path.append('/app/business/fx')
sys.path.append('/app/business')
from technical_analysis import TechnicalAnalysis
ta=TechnicalAnalysis()
results=ta.technicalIndicators(None)
st.write(results)
