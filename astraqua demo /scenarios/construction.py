"""
Smart Construction scenario configuration.

Data-only, following the same shape as scenarios/mining.py: SCENARIO,
ZONES, VEHICLES, EVENTS. Consumed by backend/simulator.py and components/.
"""

SCENARIO = {
    "id": "construction",
    "icon": "🏗️",
    "title": "Smart Construction",
    "situation": (
        "An autonomous fleet is coordinating excavation, crane lifts, and "
        "material delivery on an active high-rise construction site. "
        "GPS is unreliable near the tower structure, weather can halt "
        "crane operations without notice, and equipment paths cross "
        "constantly. AQFM must keep the site moving while keeping crews "
        "and equipment safely separated."
    ),
    "vehicles_summary": ["Site survey drones", "Autonomous excavator", "Tower crane", "Delivery robot"],
    "objectives": [
        "Complete foundation zone survey",
        "Maintain safe equipment separation",
        "Continue despite failures",
        "Optimize battery",
        "Reduce communication",
    ],
    "difficulty": 3,
    "estimated_minutes": 7,
}

ZONES = [
    {"name": "Foundation Zone", "x": 50, "y": 90},
    {"name": "Tower Crane Bay", "x": 24, "y": 56},
    {"name": "Material Yard", "x": 76, "y": 52},
    {"name": "Site Office", "x": 50, "y": 10},
]

VEHICLES = [
    {"id": "drone_1", "name": "Survey Drone 1", "type": "drone", "icon": "🚁", "x": 32, "y": 68, "battery": 91},
    {"id": "drone_2", "name": "Survey Drone 2", "type": "drone", "icon": "🚁", "x": 44, "y": 78, "battery": 87},
    {"id": "excavator_1", "name": "Excavator", "type": "excavator", "icon": "🛠️", "x": 60, "y": 40, "battery": 96},
    {"id": "crane_1", "name": "Tower Crane", "type": "crane", "icon": "🏗️", "x": 24, "y": 40, "battery": 99},
    {"id": "robot_1", "name": "Delivery Robot", "type": "robot", "icon": "🤖", "x": 68, "y": 24, "battery": 94},
]

EVENTS = [
    {
        "id": "sensor_alert",
        "label": "Structural Sensor Alert",
        "icon": "⚠️",
        "target": "excavator_1",
        "health_delta": -12,
        "bandwidth_delta": +5,
        "narrative": [
            "Ground stability sensor flagged a soft spot in the Foundation Zone.",
            "AQFM halted the excavator and rerouted its dig plan.",
            "Survey Drone 1 dispatched to re-scan the flagged area.",
        ],
        "chat_answer": (
            "A ground stability sensor flagged a soft spot in the foundation "
            "zone. AQFM stopped the excavator immediately, rerouted its dig "
            "plan, and sent a survey drone to re-scan the flagged area."
        ),
        "recovers": True,
    },
    {
        "id": "gps_multipath",
        "label": "GPS Multipath",
        "icon": "⚠️",
        "target": "crane_1",
        "health_delta": -9,
        "bandwidth_delta": +4,
        "narrative": [
            "GPS signal degraded near the tower structure due to multipath reflection.",
            "AQFM switched the crane to visual-fiducial positioning.",
            "Lift operations continued at reduced speed for precision.",
        ],
        "chat_answer": (
            "GPS near the tower crane bay was degraded by signal reflecting "
            "off the structure. AQFM switched the crane to visual-fiducial "
            "positioning and slowed lift operations slightly for precision."
        ),
        "recovers": True,
    },
    {
        "id": "weather_delay",
        "label": "Weather Delay",
        "icon": "⚠️",
        "target": "crane_1",
        "health_delta": -14,
        "bandwidth_delta": +3,
        "narrative": [
            "Wind speed near Tower Crane Bay exceeded safe lift thresholds.",
            "AQFM suspended crane lifts and secured the load.",
            "Delivery Robot re-tasked to ground-level material moves in the meantime.",
        ],
        "chat_answer": (
            "Wind speed at the tower crane bay exceeded safe lift thresholds. "
            "AQFM suspended lifts, secured the load, and re-tasked the "
            "delivery robot to ground-level moves until conditions cleared."
        ),
        "recovers": True,
    },
    {
        "id": "collision_risk",
        "label": "Equipment Collision Risk",
        "icon": "⚠️",
        "target": "robot_1",
        "health_delta": -13,
        "bandwidth_delta": +4,
        "narrative": [
            "Delivery Robot's path projected to cross the excavator's swing radius.",
            "AQFM held the robot and recalculated a clear delivery route.",
            "Excavator continued operating without interruption.",
        ],
        "chat_answer": (
            "AQFM predicted the delivery robot's path would cross the "
            "excavator's swing radius. It held the robot, recalculated a "
            "clear route, and let the excavator keep working without any "
            "interruption."
        ),
        "recovers": True,
    },
    {
        "id": "battery_critical",
        "label": "Battery Critical",
        "icon": "⚠️",
        "target": "drone_2",
        "health_delta": -8,
        "bandwidth_delta": +2,
        "narrative": [
            "Survey Drone 2 battery reserve fell below safe threshold.",
            "AQFM ordered an early return to Site Office for recharge.",
            "Coverage gap redistributed to Survey Drone 1.",
        ],
        "chat_answer": (
            "Survey Drone 2's battery fell below the safe reserve threshold, "
            "so AQFM recalled it to the site office early and redistributed "
            "its coverage to Survey Drone 1."
        ),
        "recovers": True,
    },
    {
        "id": "crane_sensor_fault",
        "label": "Crane Sensor Fault",
        "icon": "⚠️",
        "target": "crane_1",
        "health_delta": -16,
        "bandwidth_delta": +5,
        "narrative": [
            "Tower Crane load-sensor reporting inconsistent readings mid-lift.",
            "AQFM paused the lift and switched to a redundant sensor channel.",
            "Lift resumed once redundant readings were confirmed consistent.",
        ],
        "chat_answer": (
            "The tower crane's load sensor started giving inconsistent "
            "readings mid-lift. AQFM paused the lift, switched to a redundant "
            "sensor channel, and only resumed once the readings were confirmed "
            "consistent."
        ),
        "recovers": True,
    },
]
