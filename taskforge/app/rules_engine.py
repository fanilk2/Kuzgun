# app/rules_engine.py
import yaml
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent.parent / "configs" / "rules.yaml"

def load_rules():
    if not CONFIG_PATH.exists():
        return [], []
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get("rules", []), data.get("penalties", [])

def _same_activity(a_cfg: str, a_in: str) -> bool:
    return str(a_cfg or "").strip().lower() == str(a_in or "").strip().lower()

def calculate_score(activity: str, duration_min: int) -> int:
    rules, penalties = load_rules()
    total = 0

    for r in rules:
        cond = r.get("when", {}) or {}
        if _same_activity(cond.get("activity"), activity):
            if "duration_min_gte" in cond and duration_min >= cond["duration_min_gte"]:
                total += int(r.get("score_delta", 0))

    for p in penalties:
        cond = p.get("when", {}) or {}
        if _same_activity(cond.get("activity"), activity):
            if "duration_min_gt" in cond and duration_min > cond["duration_min_gt"]:
                total += int(p.get("score_delta", 0))

    return total
