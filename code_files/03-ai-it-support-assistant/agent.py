"""AI Investigation Agent: RAG + Tools + LLM reasoning."""

from __future__ import annotations

import json
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from rag import BASE_DIR, search_knowledge_base
from tools import get_application_config, get_application_logs

load_dotenv(BASE_DIR / ".env")

MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def _get_llm() -> ChatOpenAI:
    return ChatOpenAI(model=MODEL, temperature=0)


def investigate_incident(issue: str) -> dict:
    """Run the full investigation workflow for an IT incident."""
    steps: list[str] = []

    documents = search_knowledge_base(issue)
    steps.append("Troubleshooting knowledge searched")

    knowledge = "\n\n".join(doc.page_content for doc in documents)

    config = get_application_config()
    steps.append("Application configuration checked")

    logs = get_application_logs()
    steps.append("Application logs checked")

    prompt = f"""
You are an AI IT Support Engineer.

Investigate the following issue.

USER ISSUE:
{issue}

COMPANY TROUBLESHOOTING DOCUMENTS:
{knowledge}

CURRENT APPLICATION CONFIGURATION:
{json.dumps(config, indent=2)}

APPLICATION LOGS:
{logs}

Based only on the supplied information:
1. Identify the probable root cause.
2. Explain the evidence.
3. Recommend a simple solution.

Keep the answer concise and easy to understand.
"""

    response = _get_llm().invoke(prompt)
    steps.append("Incident analyzed")

    return {
        "answer": response.content,
        "steps": steps,
        "documents": documents,
        "config": config,
        "logs": logs,
    }
