import streamlit as st
import sys
from technical_analysis import TechnicalAnalysis
#sys.path.append('/app/business/fx')
sys.path.append('/app/business')
results=TechnicalAnalysis.technicalIndicators()
st.write(results)
