import streamlit as st
import pandas as pd
import numpy as np
from src import read_winds


st.write("Wind in Silvaplana since August 2024")
st.write("Source: https://www.kitesailing.ch/en/spot/webcam")

# db = pd.read_csv('../db/winds.csv', encoding='latin1', on_bad_lines='skip')
# db = db.set_index('timestamp')
# db = read_winds.WindReader().load_db()
# chart_data = pd.DataFrame(db)
# st.line_chart(chart_data)
