"""Operational tools for the AI IT Support Assistant."""

from __future__ import annotations

import json

from rag import BASE_DIR

DEMO_DATA_DIR = BASE_DIR / "demo_data"


def get_application_config() -> dict:
    """Return the current application configuration."""
    with open(DEMO_DATA_DIR / "config.json", "r", encoding="utf-8") as file:
        return json.load(file)


def get_application_logs() -> str:
    """Return the recent application log content."""
    with open(DEMO_DATA_DIR / "application.log", "r", encoding="utf-8") as file:
        return file.read()
