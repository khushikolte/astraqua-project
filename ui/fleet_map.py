import plotly.graph_objects as go
import streamlit as st


def drone_color(battery):
    if battery > 70:
        return "#22c55e"   # green
    elif battery > 30:
        return "#eab308"   # yellow
    return "#ef4444"       # red


def render_fleet_map(state):

    st.subheader("🗺️ Fleet Overview")

    fleet_size = state["fleet_size"]

    # ---------------------------
    # Vehicle Positions
    # ---------------------------

    positions = [
        (0, 0),
        (2, 1),
        (4, 0),
        (1, -2),
        (3, -2),
        (2, 3),
        (5, 2),
        (-1, 2),
    ]

    names = [
        "Drone 1",
        "Drone 2",
        "Drone 3",
        "Drone 4",
        "Drone 5",
        "Drone 6",
        "Drone 7",
        "Drone 8",
    ]

    battery = state["battery"]

    fig = go.Figure()

    # ---------------------------
    # Communication Links
    # ---------------------------

    wifi = state["wifi"]

    if wifi > 25:

        for i in range(fleet_size - 1):

            x0, y0 = positions[i]
            x1, y1 = positions[i + 1]

            fig.add_trace(
                go.Scatter(
                    x=[x0, x1],
                    y=[y0, y1],
                    mode="lines",
                    line=dict(
                        color="#4FC3F7",
                        width=3
                    ),
                    hoverinfo="skip",
                    showlegend=False,
                )
            )

    # ---------------------------
    # Drones
    # ---------------------------

    xs = []
    ys = []
    labels = []

    for i in range(fleet_size):

        x, y = positions[i]

        xs.append(x)
        ys.append(y)

        labels.append(
            f"{names[i]}<br>"
            f"Battery: {battery}%<br>"
            f"WiFi: {state['wifi']}%<br>"
            f"GPS: {state['gps']}%"
        )

    fig.add_trace(
        go.Scatter(
            x=xs,
            y=ys,
            mode="markers+text",
            text=[f"🚁 {i+1}" for i in range(fleet_size)],
            textposition="top center",
            hovertext=labels,
            hoverinfo="text",
            marker=dict(
                size=28,
                color=drone_color(battery),
                line=dict(
                    color="white",
                    width=2
                ),
            ),
            showlegend=False,
        )
    )

    # ---------------------------
    # Base Station
    # ---------------------------

    fig.add_trace(
        go.Scatter(
            x=[2],
            y=[-4],
            mode="markers+text",
            text=["🏠 Base"],
            textposition="bottom center",
            marker=dict(
                size=35,
                color="#3b82f6",
            ),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    # ---------------------------
    # Layout
    # ---------------------------

    fig.update_layout(

        template="plotly_dark",

        height=600,

        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        ),

        xaxis=dict(
            visible=False,
            range=[-2,6]
        ),

        yaxis=dict(
            visible=False,
            range=[-5,4]
        ),

        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ---------------------------
    # Mission Status
    # ---------------------------

    cols = st.columns(3)

    with cols[0]:
        if state["wifi"] > 25:
            st.success("📶 Connected")
        else:
            st.error("📶 WiFi Lost")

    with cols[1]:
        if state["gps"] > 25:
            st.success("🛰 GPS Active")
        else:
            st.warning("🛰 GPS Denied")

    with cols[2]:
        if battery > 30:
            st.success("🔋 Fleet Healthy")
        else:
            st.error("🔋 Low Battery")