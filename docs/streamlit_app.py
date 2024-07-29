import streamlit as st
import pandas as pd
import numpy as np


st.write("Wind in Silvaplana since August 2024")
st.write("Source: https://www.kitesailing.ch/en/spot/webcam")

# Read db
db = pd.read_csv('winds.csv', encoding='latin1', on_bad_lines='skip')
db = db.set_index('timestamp')

# Plot DB
chart_data = pd.DataFrame(db)
st.line_chart(chart_data)
