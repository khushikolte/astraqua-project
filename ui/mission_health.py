import streamlit as st


def render_mission_health(state):
    """
    Display the overall mission health.
    """

    wifi = state["wifi"]
    gps = state["gps"]
    battery = state["battery"]

    score = (wifi + gps + battery) / 3

    if state["weather"] == "Storm":
        score -= 20
    elif state["weather"] == "Rain":
        score -= 10

    if state["terrain"] == "Remote Area":
        score -= 10

    score = max(0, min(score, 100))

    st.subheader("🎯 Mission Health")

    if score >= 80:
        status = "🟢 Excellent"
    elif score >= 60:
        status = "🟡 Stable"
    elif score >= 40:
        status = "🟠 Warning"
    else:
        status = "🔴 Critical"

    st.metric(
        label="Mission Score",
        value=f"{score:.0f}%"
    )

    st.progress(score / 100)

    st.markdown(f"### {status}")

    st.markdown("---")

    st.write("### Current Status")

    st.write(f"📶 WiFi: **{wifi}%**")
    st.write(f"🛰 GPS: **{gps}%**")
    st.write(f"🔋 Battery: **{battery}%**")