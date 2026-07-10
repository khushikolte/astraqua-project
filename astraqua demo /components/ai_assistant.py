import streamlit as st


def render_copilot_log(sim):
    st.markdown("#### 🛰️ AQFM AI Copilot")
    log = sim.copilot_log[-8:]
    for entry in reversed(log):
        css_class = {"info": "", "alert": "alert", "critical": "critical"}[entry["level"]]
        st.markdown(
            f'<div class="copilot-msg {css_class}">{entry["text"]}</div>',
            unsafe_allow_html=True,
        )


def render_chat(sim, events_by_id, key_prefix="mining"):
    st.markdown("#### 💬 Ask AQFM")

    suggestions = [
        "Why did the fleet reroute?",
        "How is bandwidth being managed?",
        "What's the current mission status?",
    ]
    cols = st.columns(len(suggestions))
    for col, question in zip(cols, suggestions):
        if col.button(question, key=f"{key_prefix}_suggest_{question}", use_container_width=True):
            sim.ask(question, events_by_id)

    question = st.chat_input("Ask AQFM about the mission...", key=f"{key_prefix}_chat_input")
    if question:
        sim.ask(question, events_by_id)

    for msg in sim.chat_history[-6:]:
        with st.chat_message("user" if msg["role"] == "user" else "assistant"):
            st.write(msg["text"])
