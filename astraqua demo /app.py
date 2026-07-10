"""
AQFM Mission Command Center
----------------------------
An investor/demo-ready Streamlit experience for AstraQua's AQFM fleet
intelligence platform. Ships six fully interactive scenarios: Mining
Operations, Wildfire Response, Search & Rescue, Offshore Inspection,
Lunar Exploration, and Smart Construction (see scenarios/).

Run with:  streamlit run app.py
"""

import time
import streamlit as st

from scenarios import mining, wildfire, rescue, offshore, lunar, construction
from backend.simulator import MissionSimulator
from components.fleet_map import render_fleet_map
from components.metrics import render_metrics
from components.ai_assistant import render_copilot_log, render_chat
from components.timeline import render_timeline
from components.events import render_event_controls

st.set_page_config(
    page_title="AQFM Mission Command Center",
    page_icon="🛰️",
    layout="wide",
)


def load_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()

SCENARIO_MODULES = {
    "mining": mining,
    "wildfire": wildfire,
    "rescue": rescue,
    "offshore": offshore,
    "lunar": lunar,
    "construction": construction,
}

if "page" not in st.session_state:
    st.session_state.page = "landing"
if "scenario" not in st.session_state:
    st.session_state.scenario = None
if "sim" not in st.session_state:
    st.session_state.sim = None


def go_to(page):
    st.session_state.page = page
    st.rerun()


# ======================================================================
# SCREEN 1 — LANDING
# ======================================================================
def render_landing():
    st.markdown(
        """
        <div class="aqfm-hero">
            <h1>AQFM Mission Command Center</h1>
            <p class="subtitle">Autonomous Fleet Intelligence for Disconnected Operations</p>
            <p class="tagline">Experience how AQFM coordinates autonomous fleets in environments
            where cloud connectivity cannot be relied upon. Choose a real-world mission
            scenario below to begin.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")

    scenarios = [
        {"id": "mining", "icon": "🏭", "title": "Mining Operations", "ready": True,
         "blurb": "Coordinate drones, haul trucks, and excavators through GPS-denied tunnels."},
        {"id": "wildfire", "icon": "🚒", "title": "Wildfire Response", "ready": True,
         "blurb": "Direct recon drones and engines through shifting wind and smoke-blind zones."},
        {"id": "rescue", "icon": "⛑️", "title": "Search & Rescue", "ready": True,
         "blurb": "Search a collapsed structure with thermal drones and ground robots after an aftershock."},
        {"id": "offshore", "icon": "🌊", "title": "Offshore Inspection", "ready": True,
         "blurb": "Inspect subsea pipeline with ROVs and USVs over lossy acoustic comms and rough seas."},
        {"id": "lunar", "icon": "🚀", "title": "Lunar Exploration", "ready": True,
         "blurb": "Survey a shadowed crater with rovers and a relay drone through comm-delay blackouts."},
        {"id": "construction", "icon": "🏗️", "title": "Smart Construction", "ready": True,
         "blurb": "Keep excavator, crane, and delivery robot working safely around a live tower site."},
    ]

    cols = st.columns(3)
    for i, sc in enumerate(scenarios):
        with cols[i % 3]:
            st.markdown(
                f"""<div class="aqfm-card">
                        <h3>{sc['icon']} {sc['title']}</h3>
                        <p>{sc['blurb']}</p>
                    </div>""",
                unsafe_allow_html=True,
            )
            st.button(
                "Select mission" if sc["ready"] else "Coming soon",
                key=f"select_{sc['id']}",
                disabled=not sc["ready"],
                use_container_width=True,
                on_click=(lambda sid=sc["id"]: _select_scenario(sid)) if sc["ready"] else None,
            )
            st.write("")


def _select_scenario(scenario_id):
    st.session_state.scenario = scenario_id
    st.session_state.page = "briefing"


# ======================================================================
# SCREEN 2 — MISSION BRIEF
# ======================================================================
def render_briefing():
    mod = SCENARIO_MODULES[st.session_state.scenario]
    sc = mod.SCENARIO

    st.markdown(f"## {sc['icon']} {sc['title']}")
    st.markdown("#### Situation")
    st.write(sc["situation"])

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Vehicles include**")
        for v in sc["vehicles_summary"]:
            st.markdown(f"- {v}")
    with col2:
        st.markdown("**Mission Objectives**")
        for obj in sc["objectives"]:
            st.markdown(f"✅ {obj}")

    st.write("")
    col1, col2, col3 = st.columns(3)
    col1.markdown(f"**Mission Difficulty**  \n{'⭐' * sc['difficulty']}{'☆' * (5 - sc['difficulty'])}")
    col2.markdown(f"**Estimated Time**  \n{sc['estimated_minutes']} minutes")
    col3.write("")

    st.write("")
    if st.button("🚀 Start Mission", type="primary", use_container_width=True):
        st.session_state.sim = MissionSimulator(mod.SCENARIO, mod.VEHICLES, mod.ZONES)
        go_to("mission")

    if st.button("← Back to mission select", use_container_width=True):
        go_to("landing")


# ======================================================================
# SCREEN 3 — LIVE MISSION
# ======================================================================
def render_mission():
    sim = st.session_state.sim
    mod = SCENARIO_MODULES[st.session_state.scenario]
    sc = mod.SCENARIO
    events_by_id = {e["id"]: e for e in mod.EVENTS}

    st.markdown(f"## {sc['icon']} {sc['title']} — Live Mission")
    render_metrics(sim)
    st.write("")

    col_map, col_copilot = st.columns([2, 1])
    with col_map:
        render_fleet_map(sim.vehicles, mod.ZONES)
    with col_copilot:
        render_copilot_log(sim)

    st.write("")
    col_tl, col_chat = st.columns([1, 1])
    with col_tl:
        render_timeline(sim)
    with col_chat:
        render_chat(sim, events_by_id, key_prefix=sc["id"])

    st.write("")
    render_event_controls(sim, mod.EVENTS, key_prefix=sc["id"])

    st.write("")
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("⏱️ Advance Mission Clock", use_container_width=True):
            sim.tick()
            st.rerun()
    with col2:
        if st.button("🏁 End Mission", type="primary", use_container_width=True):
            go_to("summary")


# ======================================================================
# SCREEN 4 — MISSION SUMMARY
# ======================================================================
def render_summary():
    sim = st.session_state.sim
    stats = sim.summary()

    st.markdown(
        """
        <div class="summary-hero">
            <h1>✅ Mission Complete</h1>
            <p>AQFM maintained mission continuity despite multiple failures.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(3)
    tiles = [
        ("Time", stats["duration"]),
        ("Bandwidth Saved", f"{stats['bandwidth_saved']}%"),
        ("Failures Recovered", stats["failures_recovered"]),
        ("Vehicles Lost", stats["vehicles_lost"]),
        ("Mission Success", f"{stats['mission_success']}%"),
        ("Assets Returned", stats["assets_returned"]),
    ]
    for i, (label, value) in enumerate(tiles):
        with cols[i % 3]:
            st.markdown(
                f"""<div class="metric-tile">
                        <div class="label">{label}</div>
                        <div class="value">{value}</div>
                    </div>""",
                unsafe_allow_html=True,
            )
            st.write("")

    st.write("")
    if st.button("🔁 Run Another Mission", use_container_width=True, type="primary"):
        st.session_state.sim = None
        st.session_state.scenario = None
        go_to("landing")


# ======================================================================
# ROUTER
# ======================================================================
PAGES = {
    "landing": render_landing,
    "briefing": render_briefing,
    "mission": render_mission,
    "summary": render_summary,
}

PAGES[st.session_state.page]()
