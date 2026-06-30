import streamlit as st


REAL_WORLD_CONTEXT = {
    "comms_down": {
        "title": "Real-world example: communications go down",
        "intro": (
            "In regions with unreliable infrastructure — rural areas, disaster zones, "
            "or places that experience frequent network outages — local internet or "
            "cellular networks can fail suddenly due to storms, power outages, "
            "congestion, or deliberate shutdowns."
        ),
        "steps": [
            ("Drones lose contact with the central system",
             "Normally each drone checks in through wifi or cellular links. "
             "Without that, they can't receive new instructions from an operator."),
            ("Drones switch to talking to each other directly",
             "This is mesh networking — shown on the map as the lines connecting "
             "drones. Even with no internet, nearby drones can still coordinate."),
            ("Each drone makes more decisions on its own",
             "This is edge AI — the drone acts on local information instead of "
             "waiting for instructions from a server it may not be able to reach."),
            ("The fleet keeps working as a team",
             "Drones rely on direct drone-to-drone links to agree on next steps, "
             "even without a central commander."),
            ("No human needs to step in immediately",
             "The system is designed to keep the mission going automatically during "
             "the outage, only escalating to a human if conditions worsen further."),
        ],
        "tie_back": (
            "This is exactly what the Communications Down scenario simulates. "
            "Watch the connecting lines between drones, and notice the "
            "Multi-Agent Coordination confidence score rise as drones lean more "
            "heavily on talking to each other."
        ),
    },
    "gps_lost": {
        "title": "Real-world example: GPS signal is lost or jammed",
        "intro": (
            "GPS can fail in real operations due to tall buildings blocking signal "
            "in dense cities, being underground or indoors, severe weather, or "
            "intentional jamming in contested environments."
        ),
        "steps": [
            ("Drones lose their primary sense of location",
             "GPS is normally how each drone knows where it is in the world."),
            ("Drones switch to inertial navigation",
             "Onboard sensors estimate position using motion and direction instead "
             "of satellite signal — less precise, but keeps the drone oriented."),
            ("Drones cross-check position using each other",
             "Multi-agent localization lets drones compare relative positions with "
             "nearby drones to correct drift in their estimated location."),
            ("The mission trajectory is maintained",
             "Despite reduced precision, the fleet continues toward its objective "
             "rather than stopping or returning home."),
        ],
        "tie_back": (
            "This is what the GPS Lost scenario simulates. Watch the GPS-Denied "
            "Operation confidence score and the timeline log how the fleet adapts "
            "without satellite positioning."
        ),
    },
    "battery_critical": {
        "title": "Real-world example: a drone's battery runs critically low",
        "intro": (
            "Battery limits are one of the most common real-world constraints on "
            "drone missions — cold weather, long flight times, or heavier payloads "
            "all drain batteries faster than expected."
        ),
        "steps": [
            ("A drone's battery drops to a critical level",
             "The system continuously monitors battery health across the fleet."),
            ("The low-battery drone returns to base automatically",
             "Rather than risking a crash mid-mission, it's pulled out safely."),
            ("Healthy drones absorb the missing workload",
             "Remaining drones redistribute coverage so the mission isn't dropped."),
            ("Mission priorities are reassigned",
             "The fleet replans which tasks matter most given fewer active drones."),
            ("Predictive maintenance is triggered",
             "The system flags the affected drone for inspection or charging before "
             "its next mission."),
        ],
        "tie_back": (
            "This is what the Battery Critical scenario simulates. Watch the "
            "Predictive Maintenance confidence score and the timeline log the "
            "drone returning home while the rest of the fleet adapts."
        ),
    },
}


def render_real_world_context(scenario: str):
    """
    Interactive click-through walkthrough of the real-world story behind
    the currently active scenario. Designed for live demo use: advance
    through steps with Next/Previous instead of dumping all text at once.
    """
    context = REAL_WORLD_CONTEXT.get(scenario)

    if context is None:
        return

    step_key = f"rwc_step_{scenario}"
    if step_key not in st.session_state:
        st.session_state[step_key] = 0

    total_steps = len(context["steps"])
    current = st.session_state[step_key]
    current = max(0, min(current, total_steps - 1))
    st.session_state[step_key] = current

    st.subheader(f"🌍 {context['title']}")
    st.write(context["intro"])

    st.markdown("---")

    dots = " ".join(
        "●" if i == current else "○"
        for i in range(total_steps)
    )
    st.markdown(f"<div style='text-align:center; font-size:20px; letter-spacing:6px;'>{dots}</div>", unsafe_allow_html=True)

    step_title, step_detail = context["steps"][current]

    st.markdown(f"#### Step {current + 1} of {total_steps}: {step_title}")
    st.write(step_detail)

    nav_left, nav_mid, nav_right = st.columns([1, 2, 1])

    with nav_left:
        if st.button("⬅ Previous", disabled=(current == 0), key=f"prev_{scenario}", use_container_width=True):
            st.session_state[step_key] = current - 1
            st.rerun()

    with nav_right:
        if current < total_steps - 1:
            if st.button("Next ➡", key=f"next_{scenario}", use_container_width=True):
                st.session_state[step_key] = current + 1
                st.rerun()
        else:
            if st.button("Restart ↺", key=f"restart_{scenario}", use_container_width=True):
                st.session_state[step_key] = 0
                st.rerun()

    if current == total_steps - 1:
        st.markdown("---")
        st.info(context["tie_back"])