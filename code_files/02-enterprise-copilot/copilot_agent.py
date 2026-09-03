"""Enterprise Copilot orchestrator: RAG + guardrails + action tools."""

from __future__ import annotations

import json
import os
import re

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from policy import check_policy
from rag import BASE_DIR, search_knowledge
from tools import create_ticket, get_ticket_status, lookup_user

load_dotenv(BASE_DIR / ".env")

MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def _get_llm() -> ChatOpenAI:
    return ChatOpenAI(model=MODEL, temperature=0)


def _collect_citations(documents) -> list[str]:
    citations = [doc.metadata.get("source", "Unknown") for doc in documents]
    return sorted(set(citations))


def _extract_ticket_id(text: str) -> str | None:
    match = re.search(r"INC-\d{4}", text, re.IGNORECASE)
    return match.group(0).upper() if match else None


def _extract_employee_id(text: str) -> str | None:
    match = re.search(r"\bE\d{4}\b", text, re.IGNORECASE)
    return match.group(0).upper() if match else None


def run_enterprise_copilot(user_input: str) -> dict:
    """Process a user request through policy, RAG, tools, and LLM reasoning."""
    steps: list[str] = []
    actions: list[dict] = []

    policy = check_policy(user_input)
    steps.append("Policy guardrail check completed")

    if not policy["allowed"]:
        return {
            "answer": f"I cannot help with that request. {policy['reason']}",
            "steps": steps,
            "actions": actions,
            "citations": [],
        }

    docs = search_knowledge(user_input)
    steps.append("Knowledge retrieved from vector store")

    knowledge_context = "\n\n".join(doc.page_content for doc in docs)
    lowered = user_input.lower()

    if "create ticket" in lowered:
        ticket = create_ticket(title=user_input, priority="High")
        actions.append({"tool": "create_ticket", "result": ticket})
        steps.append("Action tool executed: create_ticket")

    ticket_id = _extract_ticket_id(user_input)
    if "ticket status" in lowered and ticket_id:
        status = get_ticket_status(ticket_id)
        actions.append({"tool": "get_ticket_status", "result": status})
        steps.append("Action tool executed: get_ticket_status")

    employee_id = _extract_employee_id(user_input)
    if employee_id:
        user = lookup_user(employee_id)
        actions.append({"tool": "lookup_user", "result": user})
        steps.append("Action tool executed: lookup_user")

    prompt = f"""
You are an Enterprise Copilot.

User request:
{user_input}

Retrieved enterprise knowledge:
{knowledge_context}

Tool outputs:
{json.dumps(actions, indent=2)}

Instructions:
1. Respond professionally.
2. Use only provided information.
3. If information is missing, state that clearly.
4. Provide next best action.
"""

    response = _get_llm().invoke(prompt)
    steps.append("LLM response generated")

    return {
        "answer": response.content,
        "steps": steps,
        "actions": actions,
        "citations": _collect_citations(docs),
    }
