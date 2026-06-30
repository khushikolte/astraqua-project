import streamlit as st


# Each entry: (icon, device name, "what it normally does")
DEVICES = {
    "comms_down": [
        ("📱", "Operator phone/tablet", "Sends live commands to the fleet"),
        ("📡", "Ground station radio", "Relays mission updates to all drones"),
        ("☁️", "Cloud dashboard", "Shows real-time fleet status to HQ"),
        ("🚁", "Drone-to-drone link", "Lets drones coordinate directly with each other"),
    ],
    "gps_lost": [
        ("🛰️", "GPS receiver", "Tells each drone its exact location"),
        ("🗺️", "Live map tracking", "Shows operators where each drone is"),
        ("🎯", "Auto-waypoint navigation", "Guides drones to precise coordinates"),
        ("🚁", "Inertial backup sensors", "Estimates position when GPS is unavailable"),
    ],
    "battery_critical": [
        ("🔋", "Drone battery", "Powers flight, sensors, and communication"),
        ("🚁", "Active flight", "Drone stays airborne and on-task"),
        ("📦", "Payload/sensor power", "Cameras and sensors stay running"),
        ("🏠", "Return-to-home system", "Brings the drone back safely before power runs out"),
    ],
}

SCENARIO_LABELS = {
    "comms_down": "Network / communications signal",
    "gps_lost": "GPS signal strength",
    "battery_critical": "Fleet battery level",
}


def device_status(signal_level: int, index: int, total: int):
    """
    Staggers device failures so they don't all drop at once —
    mirrors how real systems degrade gradually rather than as a single cliff.
    """
    threshold = 70 - (index * (40 / max(total - 1, 1)))

    if signal_level >= threshold + 15:
        return "🟢", "Online", "var(--text-primary)"
    elif signal_level >= threshold:
        return "🟡", "Degraded", "var(--text-secondary)"
    else:
        return "🔴", "Offline", "var(--text-secondary)"


def render_playground(scenario: str):
    """
    A hands-on widget: drag the signal slider and watch real-world devices
    and systems react live, independent of the AI model call. Meant to build
    intuition before/alongside the technical pillar confidence scores.
    """
    devices = DEVICES.get(scenario)
    label = SCENARIO_LABELS.get(scenario)

    if devices is None:
        return

    st.subheader("🎮 Try it yourself")
    st.caption("Drag the slider and watch what happens to real-world systems in this scenario.")

    slider_key = f"playground_signal_{scenario}"
    signal_level = st.slider(
        label,
        min_value=0,
        max_value=100,
        value=100,
        key=slider_key,
    )

    st.write("")

    cols = st.columns(len(devices))

    for i, (col, (icon, name, description)) in enumerate(zip(cols, devices)):
        status_icon, status_text, _ = device_status(signal_level, i, len(devices))

        with col:
            st.markdown(
                f"<div style='text-align:center; font-size:36px;'>{icon}</div>",
                unsafe_allow_html=True,
            )
            st.markdown(f"**{name}**")
            st.caption(description)
            st.markdown(f"{status_icon} **{status_text}**")

    st.write("")

    if signal_level >= 70:
        st.success("✅ All systems operating normally.")
    elif signal_level >= 40:
        st.warning("⚠️ Some systems are degraded — the fleet is starting to adapt.")
    else:
        st.error("🚨 Critical conditions — the fleet is now relying on backup behavior to keep the mission going.")