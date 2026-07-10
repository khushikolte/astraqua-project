"""
Lunar Exploration scenario configuration.

Data-only, following the same shape as scenarios/mining.py: SCENARIO,
ZONES, VEHICLES, EVENTS. Consumed by backend/simulator.py and components/.
"""

SCENARIO = {
    "id": "lunar",
    "icon": "🚀",
    "title": "Lunar Exploration",
    "situation": (
        "An autonomous fleet is surveying a permanently shadowed crater "
        "region near the lunar south pole. Earth communication has a "
        "multi-second delay and regular blackout windows, temperatures "
        "swing to extremes, and terrain is unmapped in places. AQFM must "
        "keep the survey moving without waiting on round-trip commands."
    ),
    "vehicles_summary": ["Lunar survey rovers", "Hopper probes", "Orbital relay drone"],
    "objectives": [
        "Complete crater rim survey",
        "Preserve vehicle power in extreme cold",
        "Continue despite failures",
        "Optimize battery",
        "Reduce Earth-link bandwidth",
    ],
    "difficulty": 5,
    "estimated_minutes": 9,
}

ZONES = [
    {"name": "Shackleton Crater Rim", "x": 50, "y": 90},
    {"name": "Regolith Field", "x": 24, "y": 56},
    {"name": "Lava Tube Entrance", "x": 76, "y": 52},
    {"name": "Landing Site", "x": 50, "y": 10},
]

VEHICLES = [
    {"id": "rover_1", "name": "Rover 1", "type": "rover", "icon": "🛰️", "x": 32, "y": 68, "battery": 88},
    {"id": "rover_2", "name": "Rover 2", "type": "rover", "icon": "🛰️", "x": 44, "y": 78, "battery": 84},
    {"id": "hopper_1", "name": "Hopper Probe", "type": "hopper", "icon": "🪐", "x": 62, "y": 40, "battery": 93},
    {"id": "relay_1", "name": "Orbital Relay Drone", "type": "drone", "icon": "🛸", "x": 50, "y": 55, "battery": 98},
    {"id": "rover_3", "name": "Rover 3", "type": "rover", "icon": "🛰️", "x": 68, "y": 24, "battery": 90},
]

EVENTS = [
    {
        "id": "solar_flare",
        "label": "Solar Flare",
        "icon": "⚠️",
        "target": "fleet",
        "health_delta": -11,
        "bandwidth_delta": +6,
        "narrative": [
            "Solar flare event detected; radiation levels spiking fleet-wide.",
            "AQFM ordered exposed vehicles into shielded standby postures.",
            "Non-critical sensors powered down until the flare subsided.",
        ],
        "chat_answer": (
            "A solar flare caused a radiation spike across the fleet. AQFM "
            "moved exposed vehicles into shielded standby postures and powered "
            "down non-critical sensors until the flare subsided."
        ),
        "recovers": True,
    },
    {
        "id": "comm_delay",
        "label": "Communication Delay",
        "icon": "⚠️",
        "target": "rover_2",
        "health_delta": -6,
        "bandwidth_delta": -20,
        "narrative": [
            "Rover 2 entered a permanently shadowed region with no Earth line-of-sight.",
            "AQFM continued survey decisions locally rather than waiting on uplink.",
            "Only critical status deltas queued for the next relay window.",
        ],
        "chat_answer": (
            "Rover 2 moved into a permanently shadowed region with no direct "
            "line to Earth. Rather than waiting on a multi-second round trip, "
            "AQFM kept making survey decisions locally and queued only "
            "critical updates for the next relay window."
        ),
        "recovers": True,
    },
    {
        "id": "dust_contamination",
        "label": "Dust Contamination",
        "icon": "⚠️",
        "target": "rover_1",
        "health_delta": -9,
        "bandwidth_delta": +3,
        "narrative": [
            "Fine regolith dust accumulating on Rover 1's solar array.",
            "AQFM scheduled a panel-clearing maneuver and reduced power draw.",
            "Survey pace on Rover 1 temporarily throttled.",
        ],
        "chat_answer": (
            "Fine regolith dust was building up on Rover 1's solar array. "
            "AQFM scheduled a panel-clearing maneuver and throttled its power "
            "draw until the array was clear again."
        ),
        "recovers": True,
    },
    {
        "id": "terrain_hazard",
        "label": "Terrain Hazard",
        "icon": "⚠️",
        "target": "rover_3",
        "health_delta": -14,
        "bandwidth_delta": +5,
        "narrative": [
            "Unmapped boulder field detected ahead of Rover 3 near the lava tube.",
            "AQFM recomputed a safe path around the obstacle in under 2 seconds.",
            "Hopper Probe re-tasked to scout the revised route from above.",
        ],
        "chat_answer": (
            "Rover 3 encountered an unmapped boulder field near the lava tube "
            "entrance. AQFM recalculated a safe route around it locally and "
            "sent the hopper probe ahead to scout the revised path."
        ),
        "recovers": True,
    },
    {
        "id": "power_critical",
        "label": "Power Critical",
        "icon": "⚠️",
        "target": "rover_2",
        "health_delta": -10,
        "bandwidth_delta": +2,
        "narrative": [
            "Rover 2 power reserve fell below safe threshold in extreme cold.",
            "AQFM ordered an early return to Landing Site for recharge.",
            "Coverage gap redistributed across Rover 1 and Rover 3.",
        ],
        "chat_answer": (
            "Rover 2's power dropped below the safe reserve threshold in the "
            "extreme cold, so AQFM recalled it to the landing site early and "
            "redistributed its coverage across Rover 1 and Rover 3."
        ),
        "recovers": True,
    },
    {
        "id": "wheel_fault",
        "label": "Rover Wheel Fault",
        "icon": "⚠️",
        "target": "rover_1",
        "health_delta": -17,
        "bandwidth_delta": +5,
        "narrative": [
            "Rover 1 reporting a wheel actuator fault on uneven terrain.",
            "AQFM shifted it to a reduced-speed limp mode.",
            "Remaining fleet re-planned survey coverage to absorb the slowdown.",
        ],
        "chat_answer": (
            "Rover 1 reported a wheel actuator fault. AQFM shifted it into a "
            "reduced-speed limp mode and re-planned the rest of the fleet's "
            "survey coverage so the mission absorbed the slowdown."
        ),
        "recovers": True,
    },
]
