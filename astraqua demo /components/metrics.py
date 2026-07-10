import streamlit as st


def _status_chip(sim):
    if sim.mission_health >= 90:
        return '<span class="chip chip-green">🟢 Operational</span>'
    if sim.mission_health >= 70:
        return '<span class="chip chip-amber">🟡 Degraded</span>'
    return '<span class="chip chip-red">🔴 Critical</span>'


def render_metrics(sim):
    online, total = sim.connected_assets()

    st.markdown(_status_chip(sim), unsafe_allow_html=True)
    st.write("")

    cols = st.columns(4)
    tiles = [
        ("Fleet Health", f"{sim.mission_health}%"),
        ("Mission Progress", f"{sim.progress}%"),
        ("Bandwidth Usage", f"{sim.bandwidth_usage}%"),
        ("Connected Assets", f"{online} / {total}"),
    ]
    for col, (label, value) in zip(cols, tiles):
        with col:
            st.markdown(
                f"""<div class="metric-tile">
                        <div class="label">{label}</div>
                        <div class="value">{value}</div>
                    </div>""",
                unsafe_allow_html=True,
            )
