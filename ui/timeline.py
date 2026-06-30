import streamlit as st


def render_timeline(state):
    """
    Display the mission event timeline based on mission conditions.
    """

    st.subheader("🕒 Mission Timeline")

    events = []

    events.append("✅ Mission Started")

    if state["wifi"] < 30:
        events.append("📶 WiFi signal lost")
        events.append("🤖 Edge AI activated")
        events.append("📡 Mesh communication enabled")

    if state["gps"] < 30:
        events.append("🛰 GPS denied")
        events.append("🧭 Switching to onboard navigation")

    if state["battery"] < 25:
        events.append("🔋 Low battery detected")
        events.append("🚁 Returning one drone to base")
        events.append("🔄 Mission reassigned")

    if state["weather"] == "Rain":
        events.append("🌧 Rain reducing visibility")

    if state["weather"] == "Storm":
        events.append("⛈ Severe weather detected")

    if state["terrain"] == "Remote Area":
        events.append("🏔 Operating in remote environment")

    events.append("🎯 AQFM maintaining mission")

    for event in events:
        st.info(event)