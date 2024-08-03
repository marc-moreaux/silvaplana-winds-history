import streamlit as st
import pandas as pd
import numpy as np
import altair as alt


def wind_direction2txt(angle):
    # Angle in degree to textual orientation
    directions = ['↓ N', '↙ NE', '← E', '↖ SE', '↑ S', '↗ SW', '→ W', '↘ NW']
    return directions[round(angle / 45) % 8]


st.write("Wind in Silvaplana since August 2024")
st.write("Source: https://www.kitesailing.ch/en/spot/webcam")

# Read db
db = pd.read_csv('./db/winds.csv', encoding='latin1', on_bad_lines='skip')
db = db.set_index('timestamp')

# Plot DB
chart_data = pd.DataFrame(db)
st.line_chart(chart_data)

# Plot with altAir
db = db.reset_index()
y = alt.Chart(db).encode(x='timestamp')
x1 = y.mark_line().encode(y='wind_speed')
x2 = y.mark_circle().encode(y='wind_dir')
c = (x1 + x2).resolve_scale(y='independent')
st.altair_chart(c, use_container_width=True)


st.write("  |  ".join([f"{i}: {wind_direction2txt(i)}"
                       for i in range(0, 360, 45)]))
