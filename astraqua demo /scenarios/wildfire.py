"""
Wildfire Response scenario configuration.

Data-only, following the same shape as scenarios/mining.py: SCENARIO,
ZONES, VEHICLES, EVENTS. Consumed by backend/simulator.py and components/.
"""

SCENARIO = {
    "id": "wildfire",
    "icon": "🚒",
    "title": "Wildfire Response",
    "situation": (
        "A fast-moving wildfire is threatening a residential perimeter. "
        "Smoke is degrading visibility and radio line-of-sight, and wind "
        "conditions are shifting rapidly. AQFM must coordinate aerial "
        "recon, ground engines, and retardant drops while keeping crews "
        "clear of flare-ups it can see coming before command can."
    ),
    "vehicles_summary": ["Aerial recon drones", "Autonomous fire engines", "Retardant tanker plane"],
    "objectives": [
        "Hold the containment line",
        "Keep crews out of flare-up zones",
        "Continue despite failures",
        "Optimize battery / fuel",
        "Reduce communication",
    ],
    "difficulty": 5,
    "estimated_minutes": 9,
}

ZONES = [
    {"name": "Ridge Line", "x": 50, "y": 90},
    {"name": "Canyon", "x": 24, "y": 58},
    {"name": "Containment Line", "x": 76, "y": 50},
    {"name": "Base Camp", "x": 50, "y": 10},
]

VEHICLES = [
    {"id": "drone_1", "name": "Recon Drone 1", "type": "drone", "icon": "🚁", "x": 32, "y": 70, "battery": 90},
    {"id": "drone_2", "name": "Recon Drone 2", "type": "drone", "icon": "🚁", "x": 46, "y": 80, "battery": 86},
    {"id": "engine_1", "name": "Engine 1", "type": "engine", "icon": "🚒", "x": 62, "y": 40, "battery": 96},
    {"id": "engine_2", "name": "Engine 2", "type": "engine", "icon": "🚒", "x": 70, "y": 28, "battery": 93},
    {"id": "tanker_1", "name": "Retardant Tanker", "type": "plane", "icon": "✈️", "x": 50, "y": 55, "battery": 98},
]

EVENTS = [
    {
        "id": "wind_shift",
        "label": "Wind Shift",
        "icon": "⚠️",
        "target": "tanker_1",
        "health_delta": -12,
        "bandwidth_delta": +5,
        "narrative": [
            "Sudden wind shift detected near the Ridge Line.",
            "AQFM recalculated the retardant drop trajectory in real time.",
            "Tanker rerouted to a revised drop line clear of the new fire vector.",
        ],
        "chat_answer": (
            "A wind shift changed the fire's projected path near the Ridge Line. "
            "AQFM recalculated the retardant tanker's drop trajectory immediately, "
            "keeping the containment line intact without waiting for command input."
        ),
        "recovers": True,
    },
    {
        "id": "spot_fire",
        "label": "Spot Fire",
        "icon": "⚠️",
        "target": "engine_2",
        "health_delta": -14,
        "bandwidth_delta": +4,
        "narrative": [
            "New spot fire ignited ahead of Engine 2's position.",
            "AQFM halted Engine 2 and rerouted it around the flare-up.",
            "Recon Drone 1 redirected to monitor spot fire growth.",
        ],
        "chat_answer": (
            "A spot fire ignited ahead of Engine 2. AQFM stopped it short and "
            "rerouted around the flare-up, then redirected a recon drone to "
            "monitor how fast the new fire was growing."
        ),
        "recovers": True,
    },
    {
        "id": "smoke_interference",
        "label": "Smoke Interference",
        "icon": "⚠️",
        "target": "drone_2",
        "health_delta": -9,
        "bandwidth_delta": +3,
        "narrative": [
            "Heavy smoke degrading optical visibility over the Canyon.",
            "Recon Drone 2 dropped altitude and switched to thermal imaging.",
            "AQFM weighted thermal sensor data over optical for the sector.",
        ],
        "chat_answer": (
            "Heavy smoke over the Canyon degraded optical visibility, so AQFM "
            "had Recon Drone 2 drop altitude and switch to thermal imaging "
            "until the smoke cleared."
        ),
        "recovers": True,
    },
    {
        "id": "comm_blackout",
        "label": "Communication Blackout",
        "icon": "⚠️",
        "target": "fleet",
        "health_delta": -7,
        "bandwidth_delta": -22,
        "narrative": [
            "Radio repeater near Base Camp lost power; uplink to command cut.",
            "Fleet fell back to local decision-making.",
            "Only critical status deltas queued for sync once reconnected.",
        ],
        "chat_answer": (
            "AQFM shares only critical mission updates. When the repeater went "
            "down, the fleet kept operating on local decisions and only queued "
            "critical status changes to sync once the link came back."
        ),
        "recovers": True,
    },
    {
        "id": "fuel_critical",
        "label": "Fuel Critical",
        "icon": "⚠️",
        "target": "engine_1",
        "health_delta": -8,
        "bandwidth_delta": +2,
        "narrative": [
            "Engine 1 fuel reserve fell below safe operating threshold.",
            "AQFM ordered an early return to Base Camp for refueling.",
            "Containment coverage redistributed to Engine 2.",
        ],
        "chat_answer": (
            "Engine 1's fuel dropped below the safe reserve threshold, so AQFM "
            "recalled it to Base Camp early and redistributed its containment "
            "coverage to Engine 2."
        ),
        "recovers": True,
    },
    {
        "id": "engine_failure",
        "label": "Engine Mechanical Failure",
        "icon": "⚠️",
        "target": "engine_2",
        "health_delta": -16,
        "bandwidth_delta": +5,
        "narrative": [
            "Engine 2 reporting a pump fault and halting operations.",
            "AQFM marked the position and cleared crews to a safe standoff.",
            "Remaining fleet re-planned containment coverage to absorb the loss.",
        ],
        "chat_answer": (
            "Engine 2 reported a pump fault. AQFM marked its position, cleared "
            "the area to a safe standoff distance, and re-planned the rest of "
            "the fleet's containment coverage so the line held without it."
        ),
        "recovers": True,
    },
]
