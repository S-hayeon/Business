"This the fundamental App"
import streamlit as st
from fx import main
import sys
sys.path.append('/app/business/fx')


st.write(main.message)
