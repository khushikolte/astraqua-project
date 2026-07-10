"""
Fake AQFM backend.

This simulates what a real AQFM API would report during a mission:
fleet health, vehicle status/positions, bandwidth usage, and a narrated
event log. It is deliberately backend-agnostic (plain dict-based state)
so it's trivial to swap for real API calls later -- see the docstring
at the bottom of this file.
"""

import random
import time
import copy


class MissionSimulator:
    """Holds and mutates the state of a single mission run."""

    def __init__(self, scenario, vehicles, zones):
        self.scenario = scenario
        self.zones = zones
        self.vehicles = {v["id"]: copy.deepcopy(v) for v in vehicles}
        for v in self.vehicles.values():
            v["status"] = "operational"  # operational | degraded | critical

        self.mission_health = 97
        self.bandwidth_usage = 18
        self.progress = 4
        self.started_at = time.time()
        self.elapsed_seconds = 0
        self.failures_recovered = 0
        self.vehicles_lost = 0

        self.event_log = []       # list of {t, text}
        self.copilot_log = []     # list of {level, text}
        self.chat_history = []    # list of {role, text}
        self.applied_event_ids = []

        self._log_event("Mission launched.")
        self._log_copilot("info", "AQFM monitoring fleet... 5 autonomous assets online.")
        self._log_copilot("info", "Battery utilization optimal. Bandwidth usage minimal.")

    # ---------------------------------------------------------------
    # Internal helpers
    # ---------------------------------------------------------------
    def _timestamp(self):
        total = int(self.elapsed_seconds)
        mins, secs = divmod(total, 60)
        return f"{mins:02d}:{secs:02d}"

    def _log_event(self, text):
        self.event_log.append({"t": self._timestamp(), "text": text})

    def _log_copilot(self, level, text):
        self.copilot_log.append({"level": level, "text": text})

    def _clamp(self, value, lo=0, hi=100):
        return max(lo, min(hi, value))

    # ---------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------
    def tick(self, seconds=3):
        """Advance the simulation clock with light ambient drift."""
        self.elapsed_seconds += seconds
        if self.progress < 100:
            self.progress = self._clamp(self.progress + random.randint(1, 3))
        for v in self.vehicles.values():
            if v["status"] != "critical":
                v["battery"] = self._clamp(v["battery"] - random.randint(0, 1))
        # gentle recovery drift toward baseline when nothing is on fire
        if self.mission_health < 97:
            self.mission_health = self._clamp(self.mission_health + 1)
        if self.bandwidth_usage > 18:
            self.bandwidth_usage = self._clamp(self.bandwidth_usage - 1)

    def connected_assets(self):
        total = len(self.vehicles)
        online = sum(1 for v in self.vehicles.values() if v["status"] != "critical")
        return online, total

    def inject_event(self, event):
        """Apply a scenario event to the simulation state."""
        self.elapsed_seconds += random.randint(20, 60)
        self.applied_event_ids.append(event["id"])

        self._log_event(f"{event['icon']} {event['label']} detected.")

        target = event.get("target")
        affected_ids = list(self.vehicles.keys()) if target == "fleet" else [target]

        for vid in affected_ids:
            if vid not in self.vehicles:
                continue
            v = self.vehicles[vid]
            v["status"] = "degraded"
            v["battery"] = self._clamp(v["battery"] - random.randint(2, 8))

        self.mission_health = self._clamp(self.mission_health + event["health_delta"])
        self.bandwidth_usage = self._clamp(self.bandwidth_usage + event["bandwidth_delta"])

        for line in event["narrative"]:
            self._log_event(line)
        self._log_copilot("alert" if event["health_delta"] > -14 else "critical", event["narrative"][0])
        for line in event["narrative"][1:]:
            self._log_copilot("info", line)

        # Recovery: after a beat, resolve the vehicles back to operational
        # (kept in the same call so the Streamlit rerun shows the full arc
        # via the timeline; a real backend would push this asynchronously).
        for vid in affected_ids:
            if vid not in self.vehicles:
                continue
            v = self.vehicles[vid]
            if event.get("recovers", True):
                v["status"] = "operational"

        if event.get("recovers", True):
            self.failures_recovered += 1
            recovery_gain = max(3, abs(event["health_delta"]) // 2)
            self.mission_health = self._clamp(self.mission_health + recovery_gain)
            self._log_event("Mission stabilized.")
            self._log_copilot("info", "Mission stabilized. Operator action not required.")

        self.chat_history.append({
            "role": "assistant",
            "text": event["chat_answer"],
            "auto": True,
        })

    def ask(self, question, events_by_id):
        """Very small keyword-matching 'chat' so the copilot feels responsive
        to freeform questions, without needing a real LLM call."""
        self.chat_history.append({"role": "user", "text": question})
        q = question.lower()

        best_match = None
        for eid in self.applied_event_ids:
            ev = events_by_id.get(eid)
            if not ev:
                continue
            keywords = [ev["label"].lower()] + [w for w in ev["target"].split("_")]
            if any(k in q for k in keywords):
                best_match = ev
        if best_match:
            answer = best_match["chat_answer"]
        elif "bandwidth" in q or "communication" in q or "comm" in q:
            answer = (
                "AQFM only shares critical mission updates with base. Vehicles "
                "continue making decisions locally, which minimizes bandwidth "
                "while keeping the fleet coordinated."
            )
        elif "battery" in q:
            avg_batt = int(sum(v["battery"] for v in self.vehicles.values()) / len(self.vehicles))
            answer = f"Average fleet battery is currently {avg_batt}%. AQFM reroutes low-battery vehicles home before they become a risk."
        elif "progress" in q or "status" in q or "health" in q:
            answer = f"Mission health is {self.mission_health}%, and inspection progress is at {self.progress}%. No unresolved failures at this time."
        else:
            answer = (
                "AQFM hasn't logged anything matching that yet in this mission. "
                "Try asking about a specific vehicle, or about bandwidth, battery, or mission progress."
            )

        self.chat_history.append({"role": "assistant", "text": answer, "auto": False})
        return answer

    def summary(self):
        online, total = self.connected_assets()
        return {
            "duration": self._timestamp(),
            "bandwidth_saved": max(0, 31 - self.bandwidth_usage + 18),
            "failures_recovered": self.failures_recovered,
            "vehicles_lost": self.vehicles_lost,
            "mission_success": self.mission_health,
            "assets_returned": f"{online}/{total}",
        }


# ---------------------------------------------------------------------
# Swapping in a real AQFM backend later:
#
# Replace the body of `inject_event` and `tick` with calls to the real
# API, e.g.:
#
#   response = requests.post(f"{AQFM_API_BASE}/missions/{mission_id}/events",
#                             json={"event_id": event["id"]})
#   state = response.json()
#   self.mission_health = state["mission_health"]
#   ...
#
# Keeping all state reads going through this class means the Streamlit
# UI layer never needs to change when the fake backend is swapped out.
# ---------------------------------------------------------------------
