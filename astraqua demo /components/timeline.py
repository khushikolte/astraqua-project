import streamlit as st


def render_timeline(sim):
    st.markdown("#### 🕓 Mission Timeline")
    rows = list(reversed(sim.event_log[-12:]))
    html = "".join(
        f'<div class="tl-row"><div class="tl-time">{r["t"]}</div><div>{r["text"]}</div></div>'
        for r in rows
    )
    st.markdown(html, unsafe_allow_html=True)
