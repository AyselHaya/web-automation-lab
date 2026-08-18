import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "bot"))

CHAOS_PATH = os.path.join(os.path.dirname(__file__), "..", "sandbox_site", "chaos.json")

ALL_SCENARIOS_OFF = {
    "mode": "manual",
    "seed": 42,
    "scenarios": {
        "popup": {"enabled": False, "probability": 1.0},
        "cookie_banner": {"enabled": False, "probability": 1.0},
        "captcha_gate": {"enabled": False, "probability": 1.0},
        "server_error": {"enabled": False, "probability": 0.15},
        "slow_response": {"enabled": False, "probability": 0.3, "min_delay_seconds": 2, "max_delay_seconds": 5},
        "redirect": {"enabled": False, "probability": 0.3},
        "dom_drift": {"enabled": False, "probability": 0.3},
        "blocked_click": {"enabled": False, "probability": 0.3},
    }
}

# Scenarios that roll independently on every single request need a recoverable
# probability during testing — 1.0 would mean every retry also always fails,
# making recovery mathematically impossible rather than testing real resilience.
RECOVERABLE_PROBABILITY = {
    "server_error": 0.3,
    "slow_response": 0.5,
    "redirect": 0.4,
    "dom_drift": 0.4,
    "blocked_click": 0.4,
}


def set_chaos_config(overrides=None):
    """Writes chaos.json with everything off, except any scenario names in overrides enabled at a testable probability."""
    config = json.loads(json.dumps(ALL_SCENARIOS_OFF))  # deep copy
    if overrides:
        for scenario_name in overrides:
            config["scenarios"][scenario_name]["enabled"] = True
            config["scenarios"][scenario_name]["probability"] = RECOVERABLE_PROBABILITY.get(scenario_name, 1.0)
    with open(CHAOS_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)