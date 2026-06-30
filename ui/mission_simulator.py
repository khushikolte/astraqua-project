import streamlit as st
from controls import render_controls
from fleet_map import render_fleet_map
from mission_health import render_mission_health
from timeline import render_timeline
from api_client import predict_from_controls, check_api_health
from real_world_context import render_real_world_context
from interactive_playground import render_playground

st.set_page_config(
    page_title="AQFM Mission Simulator",
    page_icon="🚁",
    layout="wide"
)
st.markdown("""
<style>
.main{ background-color:#0E1117; }
h1,h2,h3{ color:white; }
.block-container{ padding-top:1rem; }
div[data-testid="stMetric"]{ background:#1b1f2a; padding:15px; border-radius:10px; }
</style>
""", unsafe_allow_html=True)
st.title("🚁 AQFM Mission Simulator")
st.caption("Simulate mission failures and observe how AQFM responds.")
health = check_api_health()
if health is None:
    st.error(
        "⚠️ Cannot reach the AQFM API. Start it with `uvicorn main:app --reload` "
        "in the backend folder, or check the AQFM_API_URL environment variable."
    )
    st.stop()
state = render_controls()
# Pick which trained scenario model best matches the current sliders.
# This is a simple heuristic — swap in something smarter once you have
# a single unified model instead of three separate scenario models.
if state["gps"] < 30:
    scenario = "gps_lost"
elif state["wifi"] < 30:
    scenario = "comms_down"
elif state["battery"] < 25:
    scenario = "battery_critical"
else:
    scenario = "gps_lost"  # default/baseline view
result, error = predict_from_controls(
    scenario,
    state["wifi"],
    state["gps"],
    state["battery"],
    state["fleet_size"],
)
if error:
    st.error(error)
    st.stop()
left, center, right = st.columns([1, 2, 1])
with left:
    render_mission_health(state)
with center:
    render_fleet_map(state)
with right:
    render_timeline(state)
st.divider()
st.subheader("AQFM pillar confidence")
cols = st.columns(4)
for col, (pillar, value) in zip(cols, result["confidences"].items()):
    with col:
        st.metric(pillar, f"{value*100:.0f}%")
        st.progress(min(max(value, 0.0), 1.0))

st.divider()
render_playground(scenario)

st.divider()
render_real_world_context(scenario)

with st.expander("Raw API response"):
    st.json(result)