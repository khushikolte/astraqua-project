"""
Search & Rescue scenario configuration.

Data-only, following the same shape as scenarios/mining.py: SCENARIO,
ZONES, VEHICLES, EVENTS. Consumed by backend/simulator.py and components/.
"""

SCENARIO = {
    "id": "rescue",
    "icon": "⛑️",
    "title": "Search & Rescue",
    "situation": (
        "A building collapse has trapped survivors beneath unstable "
        "debris. GPS and radio are unreliable inside the rubble field, "
        "and aftershocks can shift the structure without warning. AQFM "
        "must coordinate thermal-imaging drones and ground robots to "
        "search safely while keeping human rescuers out of harm's way."
    ),
    "vehicles_summary": ["Thermal recon drones", "Ground search robots", "Rescue support helicopter"],
    "objectives": [
        "Complete debris field search",
        "Keep rescuers out of unstable zones",
        "Continue despite failures",
        "Optimize battery",
        "Reduce communication",
    ],
    "difficulty": 5,
    "estimated_minutes": 8,
}

ZONES = [
    {"name": "Collapsed Structure", "x": 50, "y": 88},
    {"name": "Debris Field", "x": 26, "y": 56},
    {"name": "Perimeter", "x": 74, "y": 54},
    {"name": "Command Post", "x": 50, "y": 10},
]

VEHICLES = [
    {"id": "drone_1", "name": "Thermal Drone 1", "type": "drone", "icon": "🚁", "x": 34, "y": 68, "battery": 92},
    {"id": "drone_2", "name": "Thermal Drone 2", "type": "drone", "icon": "🚁", "x": 44, "y": 76, "battery": 87},
    {"id": "robot_1", "name": "Search Robot 1", "type": "robot", "icon": "🤖", "x": 22, "y": 50, "battery": 90},
    {"id": "robot_2", "name": "Search Robot 2", "type": "robot", "icon": "🤖", "x": 60, "y": 44, "battery": 94},
    {"id": "heli_1", "name": "Rescue Helicopter", "type": "helicopter", "icon": "🚁", "x": 50, "y": 30, "battery": 97},
]

EVENTS = [
    {
        "id": "aftershock",
        "label": "Structural Aftershock",
        "icon": "⚠️",
        "target": "robot_1",
        "health_delta": -15,
        "bandwidth_delta": +5,
        "narrative": [
            "Aftershock detected; debris field geometry has shifted.",
            "AQFM halted Search Robot 1 and recomputed a safe path.",
            "Nearby assets warned to hold position until re-cleared.",
        ],
        "chat_answer": (
            "An aftershock shifted the debris field's geometry. AQFM stopped "
            "Search Robot 1 immediately, recomputed a safe path around the new "
            "shift, and held nearby assets in place until the area was re-cleared."
        ),
        "recovers": True,
    },
    {
        "id": "signal_loss",
        "label": "Signal Loss in Rubble",
        "icon": "⚠️",
        "target": "robot_2",
        "health_delta": -8,
        "bandwidth_delta": +3,
        "narrative": [
            "Search Robot 2 lost GPS and radio deep in the rubble.",
            "AQFM switched it to onboard inertial and visual navigation.",
            "Coverage cross-checked against Thermal Drone 2's overhead scan.",
        ],
        "chat_answer": (
            "Search Robot 2 lost GPS and radio inside the rubble pile. AQFM "
            "switched it to inertial and visual navigation, then cross-checked "
            "its coverage against an overhead thermal scan to stay on track."
        ),
        "recovers": True,
    },
    {
        "id": "survivor_detected",
        "label": "Survivor Detected",
        "icon": "⚠️",
        "target": "drone_2",
        "health_delta": -6,
        "bandwidth_delta": +6,
        "narrative": [
            "Thermal Drone 2 flagged a heat signature consistent with a survivor.",
            "AQFM re-tasked Search Robot 2 to investigate at ground level.",
            "Location and confidence score queued for priority sync to Command Post.",
        ],
        "chat_answer": (
            "Thermal Drone 2 detected a heat signature matching a possible "
            "survivor. AQFM re-tasked Search Robot 2 to investigate at ground "
            "level and prioritized that location for sync back to Command Post."
        ),
        "recovers": True,
    },
    {
        "id": "toxic_gas",
        "label": "Toxic Gas Reading",
        "icon": "⚠️",
        "target": "robot_1",
        "health_delta": -13,
        "bandwidth_delta": +4,
        "narrative": [
            "Search Robot 1 detected elevated gas readings in its sector.",
            "AQFM withdrew the robot and flagged the zone as unsafe for humans.",
            "Search plan rerouted around the flagged zone.",
        ],
        "chat_answer": (
            "Search Robot 1 picked up elevated toxic gas readings. AQFM pulled "
            "it out immediately, flagged that zone as unsafe for human rescuers, "
            "and rerouted the search plan around it."
        ),
        "recovers": True,
    },
    {
        "id": "battery_critical",
        "label": "Battery Critical",
        "icon": "⚠️",
        "target": "drone_1",
        "health_delta": -9,
        "bandwidth_delta": +2,
        "narrative": [
            "Thermal Drone 1 battery reserve fell below safe threshold.",
            "AQFM ordered an early return to Command Post for recharge.",
            "Coverage gap redistributed to Thermal Drone 2.",
        ],
        "chat_answer": (
            "Thermal Drone 1's battery fell below the safe reserve threshold, "
            "so AQFM recalled it to Command Post early and redistributed its "
            "coverage to Thermal Drone 2."
        ),
        "recovers": True,
    },
    {
        "id": "robot_stuck",
        "label": "Robot Stuck in Debris",
        "icon": "⚠️",
        "target": "robot_2",
        "health_delta": -17,
        "bandwidth_delta": +5,
        "narrative": [
            "Search Robot 2 wedged against unstable debris and stopped moving.",
            "AQFM commanded a controlled reverse-and-reroute maneuver.",
            "Rescue Helicopter repositioned to keep visual on the robot's status.",
        ],
        "chat_answer": (
            "Search Robot 2 got wedged against unstable debris. AQFM commanded "
            "a controlled reverse-and-reroute maneuver to free it, and moved "
            "the rescue helicopter overhead to keep visual confirmation on it."
        ),
        "recovers": True,
    },
]
