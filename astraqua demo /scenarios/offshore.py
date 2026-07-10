"""
Offshore Inspection scenario configuration.

Data-only, following the same shape as scenarios/mining.py: SCENARIO,
ZONES, VEHICLES, EVENTS. Consumed by backend/simulator.py and components/.
"""

SCENARIO = {
    "id": "offshore",
    "icon": "🌊",
    "title": "Offshore Inspection",
    "situation": (
        "An autonomous fleet is inspecting subsea pipeline and platform "
        "infrastructure far from shore. Satellite bandwidth is expensive "
        "and unreliable, underwater comms are acoustic-only and lossy, "
        "and sea state can change fast. AQFM must keep the inspection "
        "moving while minimizing costly uplink traffic."
    ),
    "vehicles_summary": ["Subsea inspection ROVs", "Surface autonomous vessels (USVs)", "Platform inspection drone"],
    "objectives": [
        "Complete pipeline corridor inspection",
        "Maintain fleet safety in rough seas",
        "Continue despite failures",
        "Optimize battery",
        "Reduce satellite bandwidth",
    ],
    "difficulty": 4,
    "estimated_minutes": 8,
}

ZONES = [
    {"name": "Platform Alpha", "x": 50, "y": 90},
    {"name": "Pipeline Corridor", "x": 24, "y": 55},
    {"name": "Subsea Manifold", "x": 76, "y": 52},
    {"name": "Support Vessel", "x": 50, "y": 10},
]

VEHICLES = [
    {"id": "rov_1", "name": "ROV 1", "type": "rov", "icon": "🤿", "x": 32, "y": 68, "battery": 89},
    {"id": "rov_2", "name": "ROV 2", "type": "rov", "icon": "🤿", "x": 44, "y": 78, "battery": 85},
    {"id": "usv_1", "name": "USV 1", "type": "usv", "icon": "🚤", "x": 60, "y": 38, "battery": 95},
    {"id": "usv_2", "name": "USV 2", "type": "usv", "icon": "🚤", "x": 68, "y": 24, "battery": 92},
    {"id": "drone_1", "name": "Platform Drone", "type": "drone", "icon": "🚁", "x": 50, "y": 55, "battery": 97},
]

EVENTS = [
    {
        "id": "rough_seas",
        "label": "Rough Seas",
        "icon": "⚠️",
        "target": "usv_1",
        "health_delta": -13,
        "bandwidth_delta": +5,
        "narrative": [
            "Sea state rising rapidly near Support Vessel.",
            "AQFM slowed USV 1 and adjusted heading to reduce wave impact.",
            "Platform Drone held position to avoid launching in high wind.",
        ],
        "chat_answer": (
            "Rising sea state near the support vessel put USV 1 at risk of "
            "excessive wave impact. AQFM slowed it and adjusted heading, and "
            "held the platform drone on deck rather than launching into the wind."
        ),
        "recovers": True,
    },
    {
        "id": "subsea_comm_loss",
        "label": "Subsea Comm Loss",
        "icon": "⚠️",
        "target": "rov_2",
        "health_delta": -10,
        "bandwidth_delta": -18,
        "narrative": [
            "Acoustic link to ROV 2 degraded near the Subsea Manifold.",
            "ROV 2 fell back to a pre-programmed local inspection pattern.",
            "Only critical status pings queued for the next acoustic window.",
        ],
        "chat_answer": (
            "Acoustic comms to ROV 2 degraded near the subsea manifold. AQFM "
            "had it fall back to a pre-programmed local inspection pattern and "
            "queued only critical status pings for the next acoustic window."
        ),
        "recovers": True,
    },
    {
        "id": "current_drift",
        "label": "Current Drift",
        "icon": "⚠️",
        "target": "rov_1",
        "health_delta": -9,
        "bandwidth_delta": +3,
        "narrative": [
            "Unexpected subsea current pushing ROV 1 off its inspection line.",
            "AQFM recalculated thrust compensation to hold position.",
            "Inspection pass extended slightly to recover lost coverage.",
        ],
        "chat_answer": (
            "An unexpected subsea current pushed ROV 1 off its inspection "
            "line. AQFM recalculated thrust compensation to hold position and "
            "extended the pass slightly to recover the coverage it lost."
        ),
        "recovers": True,
    },
    {
        "id": "corrosion_anomaly",
        "label": "Corrosion Anomaly Detected",
        "icon": "⚠️",
        "target": "rov_2",
        "health_delta": -5,
        "bandwidth_delta": +7,
        "narrative": [
            "ROV 2 flagged a corrosion anomaly on the Pipeline Corridor segment.",
            "AQFM queued high-resolution imagery for priority satellite sync.",
            "USV 2 re-tasked to relay the imagery when in range.",
        ],
        "chat_answer": (
            "ROV 2 flagged a corrosion anomaly along the pipeline corridor. "
            "AQFM queued high-resolution imagery of it for priority satellite "
            "sync and re-tasked USV 2 to relay it once back in range."
        ),
        "recovers": True,
    },
    {
        "id": "battery_critical",
        "label": "Battery Critical",
        "icon": "⚠️",
        "target": "rov_1",
        "health_delta": -8,
        "bandwidth_delta": +2,
        "narrative": [
            "ROV 1 battery reserve fell below safe threshold.",
            "AQFM ordered an early return to Support Vessel for recharge.",
            "Coverage gap redistributed to ROV 2.",
        ],
        "chat_answer": (
            "ROV 1's battery fell below the safe reserve threshold, so AQFM "
            "recalled it to the support vessel early and redistributed its "
            "coverage to ROV 2."
        ),
        "recovers": True,
    },
    {
        "id": "tether_snag",
        "label": "ROV Tether Snag",
        "icon": "⚠️",
        "target": "rov_2",
        "health_delta": -16,
        "bandwidth_delta": +4,
        "narrative": [
            "ROV 2's tether snagged on platform structure near Platform Alpha.",
            "AQFM commanded a controlled backtrack to release tension.",
            "USV 1 repositioned to keep the tether path clear.",
        ],
        "chat_answer": (
            "ROV 2's tether snagged on the platform structure. AQFM commanded "
            "a controlled backtrack to release the tension and repositioned "
            "USV 1 to keep the tether path clear going forward."
        ),
        "recovers": True,
    },
]
