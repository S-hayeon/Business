"This the fundamental App"
import streamlit as st

import sys
sys.path.append('/app/business/fx')
#from fx import main
import main

st.write(main.message)
