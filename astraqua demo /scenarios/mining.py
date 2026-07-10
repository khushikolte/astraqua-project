"""
Mining Operations scenario configuration.

This module is intentionally data-only: vehicle roster, starting map
positions, zone labels, and the catalogue of injectable events. The
simulation logic that consumes this data lives in backend/simulator.py.
"""

SCENARIO = {
    "id": "mining",
    "icon": "🏭",
    "title": "Mining Operations",
    "situation": (
        "An autonomous fleet is inspecting an active mining site. "
        "Connectivity is intermittent due to underground tunnels, terrain, "
        "and limited network infrastructure. AQFM must coordinate the fleet "
        "locally while minimizing bandwidth usage and ensuring mission success."
    ),
    "vehicles_summary": ["Inspection drones", "Autonomous haul trucks", "Robotic excavators"],
    "objectives": [
        "Complete site inspection",
        "Maintain fleet safety",
        "Continue despite failures",
        "Optimize battery",
        "Reduce communication",
    ],
    "difficulty": 4,  # out of 5
    "estimated_minutes": 8,
}

# Static map zones (for background labels on the mission map)
ZONES = [
    {"name": "Mountain Ridge", "x": 50, "y": 92},
    {"name": "Tunnel A", "x": 22, "y": 60},
    {"name": "Rock Wall", "x": 78, "y": 55},
    {"name": "Base", "x": 50, "y": 8},
]

# Vehicle roster with starting positions on a 0-100 x/y grid
VEHICLES = [
    {"id": "drone_1", "name": "Drone 1", "type": "drone", "icon": "🚁", "x": 30, "y": 68, "battery": 91},
    {"id": "drone_2", "name": "Drone 2", "type": "drone", "icon": "🚁", "x": 42, "y": 78, "battery": 88},
    {"id": "drone_3", "name": "Drone 3", "type": "drone", "icon": "🚁", "x": 20, "y": 55, "battery": 84},
    {"id": "truck_1", "name": "Haul Truck", "type": "truck", "icon": "🚚", "x": 60, "y": 35, "battery": 95},
    {"id": "excavator_1", "name": "Excavator", "type": "excavator", "icon": "🛠️", "x": 68, "y": 22, "battery": 97},
]

# Injectable events. Each defines a human-readable operational narrative,
# the mission-health / bandwidth impact, and which vehicle(s) it affects.
EVENTS = [
    {
        "id": "tunnel_gps_loss",
        "label": "Tunnel GPS Loss",
        "icon": "⚠️",
        "target": "drone_3",
        "health_delta": -8,
        "bandwidth_delta": +4,
        "narrative": [
            "GPS unavailable near Tunnel A.",
            "AQFM switched Drone 3 to visual localization.",
            "Inspection reassigned to Drone 2.",
            "Mission delay: 12 seconds. Operator action not required.",
        ],
        "chat_answer": (
            "Drone 3 entered a GPS-denied tunnel. AQFM predicted localization "
            "confidence would decrease, so inspection was reassigned to Drone 2 "
            "while Drone 3 switched to onboard visual localization. Mission "
            "completion remained unaffected."
        ),
        "recovers": True,
    },
    {
        "id": "rockslide",
        "label": "Rockslide",
        "icon": "⚠️",
        "target": "truck_1",
        "health_delta": -14,
        "bandwidth_delta": +6,
        "narrative": [
            "Debris detected on Haul Truck's planned route near Rock Wall.",
            "AQFM recomputed a safe detour in under 2 seconds.",
            "Haul Truck rerouted; excavator holds position as a precaution.",
        ],
        "chat_answer": (
            "A rockslide blocked the haul truck's route near the Rock Wall zone. "
            "AQFM recalculated a detour locally, without needing operator input, "
            "and paused the excavator nearby as a safety precaution."
        ),
        "recovers": True,
    },
    {
        "id": "dust_storm",
        "label": "Dust Storm",
        "icon": "⚠️",
        "target": "drone_2",
        "health_delta": -10,
        "bandwidth_delta": +3,
        "narrative": [
            "Visibility dropping across Sector A due to dust storm.",
            "Drone 2 descended to a safer altitude and slowed inspection pace.",
            "AQFM increased sensor fusion weighting on LIDAR over optical.",
        ],
        "chat_answer": (
            "A dust storm reduced optical visibility across Sector A. AQFM had "
            "Drone 2 descend to a safer altitude and leaned more heavily on "
            "LIDAR rather than optical sensors until visibility recovered."
        ),
        "recovers": True,
    },
    {
        "id": "comm_blackout",
        "label": "Communication Blackout",
        "icon": "⚠️",
        "target": "fleet",
        "health_delta": -6,
        "bandwidth_delta": -20,
        "narrative": [
            "Uplink to base lost across the fleet.",
            "Vehicles fell back to local decision-making.",
            "Only critical status deltas queued for sync once reconnected.",
        ],
        "chat_answer": (
            "AQFM shares only critical mission updates. During the blackout, "
            "vehicles continued making decisions locally and only critical "
            "status deltas were queued for sync, which is why the mission "
            "didn't stall even though communication with base was cut."
        ),
        "recovers": True,
    },
    {
        "id": "battery_critical",
        "label": "Vehicle Battery Critical",
        "icon": "⚠️",
        "target": "drone_1",
        "health_delta": -9,
        "bandwidth_delta": +2,
        "narrative": [
            "Drone 1 battery reserve fell below safe threshold.",
            "AQFM ordered an early return to Base for recharge.",
            "Coverage gap redistributed across Drone 2 and Drone 3.",
        ],
        "chat_answer": (
            "Drone 1's battery fell below the safe reserve threshold, so AQFM "
            "recalled it to base early. Its remaining inspection coverage was "
            "automatically redistributed across Drone 2 and Drone 3."
        ),
        "recovers": True,
    },
    {
        "id": "drone_failure",
        "label": "Drone Failure",
        "icon": "⚠️",
        "target": "drone_2",
        "health_delta": -16,
        "bandwidth_delta": +5,
        "narrative": [
            "Drone 2 reporting a rotor fault and requesting emergency landing.",
            "AQFM cleared a safe landing zone near Base.",
            "Remaining fleet re-planned coverage to absorb the loss.",
        ],
        "chat_answer": (
            "Drone 2 reported a rotor fault. AQFM immediately cleared a safe "
            "landing zone near base and re-planned the remaining fleet's "
            "coverage so the inspection mission could continue without it."
        ),
        "recovers": True,
    },
]
