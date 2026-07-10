import streamlit as st


def render_event_controls(sim, events, key_prefix="mining"):
    st.markdown("#### ⚠️ Inject Event")
    cols = st.columns(4)
    for i, event in enumerate(events):
        col = cols[i % 4]
        with col:
            already_used = event["id"] in sim.applied_event_ids
            label = f"{event['icon']} {event['label']}"
            if col.button(
                label,
                key=f"{key_prefix}_event_{event['id']}",
                use_container_width=True,
                disabled=already_used,
            ):
                sim.inject_event(event)
                st.rerun()
