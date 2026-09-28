"""Belief-Desire-Intention (BDI) Deliberation Engine
100% Python Standard Library.
"""

class BDIAgent:
    """BDI agent reasoning cycle with plan library and intention filter."""
    def __init__(self):
        self.beliefs = {}
        self.desires = []
        self.intentions = []
        self.plan_library = {
            "find_energy": ["navigate_to_charger", "connect_plug", "recharge"],
            "collect_sample": ["navigate_to_rock", "deploy_arm", "store_sample"]
        }

    def update_beliefs(self, percepts):
        self.beliefs.update(percepts)
        self.desires = []
        if self.beliefs.get("battery_level", 100) < 20:
            self.desires.append("find_energy")
        if self.beliefs.get("target_detected", False):
            self.desires.append("collect_sample")

    def filter_intentions(self):
        if "find_energy" in self.desires:
            self.intentions = list(self.plan_library["find_energy"])
        elif "collect_sample" in self.desires:
            self.intentions = list(self.plan_library["collect_sample"])
        else:
            self.intentions = []
        return self.intentions

    def step(self):
        if not self.intentions:
            return "idle"
        return self.intentions.pop(0)
