"""Scoring utilities for TaskForge entries."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Tuple

import yaml

CONFIG_PATH = Path(__file__).resolve().parent.parent / "configs" / "rules.yaml"


def load_rules() -> Tuple[list, list]:
    """Return (rules, penalties) tuples from the YAML configuration."""

    if not CONFIG_PATH.exists():
        return [], []

    with open(CONFIG_PATH, "r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}

    return data.get("rules", []), data.get("penalties", [])


def _normalize(value: str | None) -> str:
    return str(value or "").strip().lower()


def _same_text(expected: str | None, actual: str | None) -> bool:
    return _normalize(expected) == _normalize(actual)


def _tags_match(rule_tags: Iterable[str] | None, entry_tags: Iterable[str] | None) -> bool:
    if not rule_tags:
        return True
    if not entry_tags:
        return False
    rule_set = {_normalize(tag) for tag in rule_tags}
    entry_set = {_normalize(tag) for tag in entry_tags}
    return not rule_set.isdisjoint(entry_set)


def _matches(cond: dict, *, activity: str, category: str | None, tags: Iterable[str] | None) -> bool:
    if cond.get("activity") and not _same_text(cond.get("activity"), activity):
        return False
    if cond.get("category") and not _same_text(cond.get("category"), category):
        return False
    if not _tags_match(cond.get("tags_any"), tags):
        return False
    return True


def _block_count(duration_min: int, per_minutes: int) -> int:
    if duration_min <= 0:
        return 0
    if per_minutes <= 0:
        per_minutes = 10
    return duration_min // per_minutes


def calculate_score(
    activity: str,
    duration_min: int,
    *,
    category: str | None = None,
    tags: Iterable[str] | None = None,
) -> int:
    """Calculate score according to the configured rules.

    Supported rule fields:
      * when.activity / when.category / when.tags_any
      * per_minutes (defaults to 10)
      * points_per_10_min (alias: points_per_block)
      * points_delta (flat bonus or penalty)
    """

    if duration_min <= 0:
        return 0

    rules, penalties = load_rules()
    total = 0

    def apply(rule: dict) -> None:
        nonlocal total
        cond = rule.get("when", {}) or {}
        if not _matches(cond, activity=activity, category=category, tags=tags):
            return

        per_minutes = int(rule.get("per_minutes", 10))
        block_points = rule.get("points_per_10_min", rule.get("points_per_block"))
        if block_points is not None:
            blocks = _block_count(duration_min, per_minutes)
            total += blocks * int(block_points)

        if "points_delta" in rule:
            total += int(rule.get("points_delta", 0))

    for rule in rules:
        apply(rule)

    for rule in penalties:
        apply(rule)

    return total
