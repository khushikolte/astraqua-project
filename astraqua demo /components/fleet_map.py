import plotly.graph_objects as go
import streamlit as st

STATUS_COLOR = {
    "operational": "#22C55E",
    "degraded": "#F59E0B",
    "critical": "#EF4444",
}


def render_fleet_map(vehicles, zones, key="fleet_map"):
    """Render the mission map: zone labels in the background, vehicles as
    colored, icon-labeled markers on top. Colors reflect live status."""

    fig = go.Figure()

    # Zone labels (static backdrop)
    fig.add_trace(go.Scatter(
        x=[z["x"] for z in zones],
        y=[z["y"] for z in zones],
        mode="text",
        text=[z["name"] for z in zones],
        textfont=dict(size=13, color="#5C6B7A"),
        hoverinfo="skip",
        showlegend=False,
    ))

    # Vehicles
    xs = [v["x"] for v in vehicles.values()]
    ys = [v["y"] for v in vehicles.values()]
    icons = [v["icon"] for v in vehicles.values()]
    colors = [STATUS_COLOR[v["status"]] for v in vehicles.values()]
    labels = [f"{v['name']} · {v['status'].title()} · {v['battery']}%" for v in vehicles.values()]

    fig.add_trace(go.Scatter(
        x=xs, y=ys,
        mode="markers+text",
        text=icons,
        textposition="middle center",
        textfont=dict(size=22),
        marker=dict(size=42, color=colors, opacity=0.25, line=dict(width=2, color=colors)),
        hovertext=labels,
        hoverinfo="text",
        showlegend=False,
    ))

    fig.update_layout(
        height=420,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.02)",
        xaxis=dict(visible=False, range=[0, 100]),
        yaxis=dict(visible=False, range=[0, 100]),
    )

    st.plotly_chart(fig, use_container_width=True, key=key, config={"displayModeBar": False})
