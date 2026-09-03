"""Policy guardrail checks for the Enterprise Copilot."""

from __future__ import annotations

import json
from pathlib import Path

from rag import BASE_DIR

POLICY_RULES_PATH = BASE_DIR / "demo_data" / "policy_rules.json"


def load_policy_rules() -> dict:
    with open(POLICY_RULES_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def check_policy(question: str) -> dict:
    """Return whether the request is allowed under policy rules."""
    rules = load_policy_rules()
    text = question.lower()

    for keyword in rules["blocked_keywords"]:
        if keyword in text:
            return {
                "allowed": False,
                "reason": f"Request blocked by policy keyword: {keyword}",
            }

    return {"allowed": True, "reason": "Allowed"}
