"""Business tools for the Enterprise Copilot demo."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from rag import BASE_DIR

DEMO_DATA_DIR = BASE_DIR / "demo_data"


def load_users() -> list[dict]:
    with open(DEMO_DATA_DIR / "users.json", "r", encoding="utf-8") as file:
        return json.load(file)


def load_tickets() -> list[dict]:
    with open(DEMO_DATA_DIR / "tickets.json", "r", encoding="utf-8") as file:
        return json.load(file)


def lookup_user(employee_id: str) -> dict:
    for user in load_users():
        if user["employee_id"] == employee_id:
            return user
    return {"error": "User not found"}


def get_ticket_status(ticket_id: str) -> dict:
    for ticket in load_tickets():
        if ticket["ticket_id"] == ticket_id:
            return ticket
    return {"error": "Ticket not found"}


def create_ticket(title: str, priority: str = "Medium") -> dict:
    ticket_id = f"INC-{datetime.now(timezone.utc).strftime('%H%M%S')}"
    return {
        "ticket_id": ticket_id,
        "title": title,
        "status": "New",
        "priority": priority,
        "message": "Ticket created in demo mode",
    }
