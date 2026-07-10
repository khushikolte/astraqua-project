# AQFM Mission Command Center

An investor/demo-ready Streamlit experience for AstraQua's AQFM fleet
intelligence platform: pick a mission → read the briefing → watch an
animated fleet map → inject real-world failures → watch AQFM narrate
its own recovery → get a mission summary.

## Run it

```bash
cd astraqua-demo
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit prints (usually `http://localhost:8501`).

## What's implemented right now

- **Landing page** with 6 mission cards, all fully interactive: Mining
  Operations, Wildfire Response, Search & Rescue, Offshore Inspection,
  Lunar Exploration, and Smart Construction.
- **Mission briefing** screen with situation, objectives, difficulty,
  and estimated time.
- **Live mission** screen:
  - Animated fleet map (Plotly) with color-coded vehicle status
  - Mission health / progress / bandwidth / connected-assets tiles
  - AQFM AI Copilot narrative log
  - Timestamped mission timeline
  - "Ask AQFM" chat (keyword-matched against the mission's own event
    log, so answers reference what actually happened in *this* run)
  - Event injection buttons (Tunnel GPS Loss, Rockslide, Dust Storm,
    Communication Blackout, Battery Critical, Drone Failure)
- **Mission summary** screen with final stats.

## Project structure

```
astraqua-demo/
├── app.py                  # main router / all 4 screens
├── styles.css              # dark mission-control theme
├── requirements.txt
├── .streamlit/config.toml  # dark theme + accent color
├── backend/
│   └── simulator.py        # fake AQFM backend (MissionSimulator)
├── components/
│   ├── fleet_map.py         # animated map
│   ├── metrics.py           # status tiles
│   ├── ai_assistant.py      # copilot log + chat
│   ├── timeline.py           # timestamped event list
│   └── events.py            # event injection buttons
└── scenarios/
    ├── mining.py              # vehicle roster, zones, event catalogue
    ├── wildfire.py
    ├── rescue.py
    ├── offshore.py
    ├── lunar.py
    └── construction.py
```

## Adding another scenario

1. Duplicate any file in `scenarios/` → `scenarios/your_scenario.py` and edit:
   `SCENARIO`, `ZONES`, `VEHICLES`, `EVENTS`.
2. In `app.py`:
   - `from scenarios import your_scenario`
   - Add it to the `SCENARIO_MODULES` dict (id → module).
   - Add a card for it in `render_landing()`'s `scenarios` list with
     `"ready": True`.
3. No changes needed to `backend/simulator.py` or `components/` — they're
   already scenario-agnostic and driven entirely by the data you pass in.
   `render_briefing()` / `render_mission()` already branch on
   `st.session_state.scenario` via `SCENARIO_MODULES`, so any new
   scenario just works.

## Swapping in the real AQFM backend

All simulated state lives in `backend/simulator.py`'s `MissionSimulator`
class. Nothing in `app.py` or `components/` talks to the backend directly —
they only read the `sim` object's attributes and call `sim.tick()` /
`sim.inject_event()` / `sim.ask()`. To connect to a real AQFM API:

1. Replace the bodies of `tick()` and `inject_event()` with real HTTP
   calls to the AQFM API (a commented example is at the bottom of
   `simulator.py`).
2. Replace `ask()`'s keyword matching with a real call to whatever
   NL layer AQFM exposes (or route it through the Anthropic API for a
   true LLM-backed copilot).

## Notes for tomorrow's meeting

- The whole app runs locally, no internet/API keys required — good for
  a laptop demo with unreliable venue wifi.
- If you want it prettier for videos/screenshots, `styles.css` has all
  the color variables at the top (`--aqfm-green`, `--aqfm-amber`, etc.)
  and is the only place you need to touch for a rebrand.
- Event buttons disable themselves once used, so you don't double-fire
  a failure mid-demo. Use "Advance Mission Clock" between events to show
  ambient progress ticking up.
