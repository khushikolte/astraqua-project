import streamlit as st


def initialize_state():
    """Initialize default values once."""

    defaults = {
        "wifi": 100,
        "gps": 100,
        "battery": 90,
        "weather": "Sunny",
        "terrain": "Urban",
        "fleet_size": 5,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_controls():

    initialize_state()

    st.sidebar.title("🎮 Mission Controls")

    st.sidebar.markdown("---")

    st.sidebar.subheader("Quick Scenarios")

    col1, col2 = st.sidebar.columns(2)

    if col1.button("📶 WiFi Failure", use_container_width=True):
        st.session_state.wifi = 10

    if col2.button("🛰 GPS Failure", use_container_width=True):
        st.session_state.gps = 10

    if st.sidebar.button("🔋 Battery Critical", use_container_width=True):
        st.session_state.battery = 15

    if st.sidebar.button("🔄 Reset Mission", use_container_width=True):
        st.session_state.wifi = 100
        st.session_state.gps = 100
        st.session_state.battery = 90
        st.session_state.weather = "Sunny"
        st.session_state.terrain = "Urban"
        st.session_state.fleet_size = 5

    st.sidebar.markdown("---")

    st.sidebar.subheader("Environment")

    wifi = st.sidebar.slider(
        "📶 WiFi Signal",
        0,
        100,
        key="wifi"
    )

    gps = st.sidebar.slider(
        "🛰 GPS Signal",
        0,
        100,
        key="gps"
    )

    battery = st.sidebar.slider(
        "🔋 Fleet Battery",
        0,
        100,
        key="battery"
    )

    weather = st.sidebar.selectbox(
        "🌦 Weather",
        [
            "Sunny",
            "Cloudy",
            "Rain",
            "Storm"
        ],
        key="weather"
    )

    terrain = st.sidebar.selectbox(
        "🌍 Terrain",
        [
            "Urban",
            "Forest",
            "Remote Area",
            "Open Water"
        ],
        key="terrain"
    )

    fleet = st.sidebar.slider(
        "🚁 Fleet Size",
        3,
        8,
        key="fleet_size"
    )

    return {
        "wifi": wifi,
        "gps": gps,
        "battery": battery,
        "weather": weather,
        "terrain": terrain,
        "fleet_size": fleet,
    }