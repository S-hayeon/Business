"This the fundamental App"
import os

# Get the absolute path of the 'fx' folder
fd_path = os.path.abspath("fx")
import streamlit as st
from fx import main

st.write(main.message)
