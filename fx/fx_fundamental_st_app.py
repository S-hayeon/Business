"This the fundamental App"
import streamlit as st

import sys
#sys.path.append('/app/business/fx')
sys.path.append('/app/business')
#from fx import main
from fx import main

st.write(main.message)
