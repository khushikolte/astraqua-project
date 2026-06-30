import streamlit as st

from ui.controls import render_controls
from ui.fleet_map import render_fleet_map
from ui.mission_health import render_mission_health
from ui.timeline import render_timeline

# --------------------------
# Page Configuration
# --------------------------

st.set_page_config(
    page_title="AQFM Mission Simulator",
    page_icon="🚁",
    layout="wide"
)

# --------------------------
# Dark Theme (custom CSS)
# --------------------------

st.markdown("""
<style>

.main{
    background-color:#0E1117;
}

h1,h2,h3{
    color:white;
}

.block-container{
    padding-top:1rem;
}

div[data-testid="stMetric"]{
    background:#1b1f2a;
    padding:15px;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------
# Title
# --------------------------

st.title("🚁 AQFM Mission Simulator")

st.caption(
    "Simulate mission failures and observe how AQFM responds."
)

# --------------------------
# Sidebar
# --------------------------

state = render_controls()

# --------------------------
# Layout
# --------------------------

left, center, right = st.columns(
    [1,2,1]
)

with left:

    render_mission_health(state)

with center:

    render_fleet_map(state)

with right:

    render_timeline(state)