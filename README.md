# Webinar RAG Agent Labs

Hands-on labs for practical enterprise AI patterns — from simple RAG Q&A to policy-aware copilots and agent-driven IT investigation.

Working application code lives under `code_files/`. Step-by-step lab guides live under `labs/`. Supporting reading material lives under `references/`.

## Concepts

### AI (Artificial Intelligence)

AI is the broad field of building systems that can perform tasks requiring human-like intelligence, such as understanding language, reasoning, summarizing, and decision support.

In these labs, AI is mainly used through Large Language Models (LLMs) to interpret user questions and generate useful responses.

### RAG (Retrieval-Augmented Generation)

RAG combines two capabilities:

1. **Retrieval** — find relevant information from private/internal documents.
2. **Generation** — use the retrieved context with an LLM to produce a grounded answer.

Why it matters:

- LLMs alone may not know your company-specific data.
- RAG improves accuracy by grounding answers in trusted sources.
- RAG helps provide traceability through citations.

### AI Agents

AI agents extend basic Q&A by adding workflow and actions:

- LLM for reasoning
- RAG for knowledge grounding
- Tools for actions (config/logs lookup, ticket creation, directory lookup)
- Workflow to sequence the steps

Agents are useful when the goal is not just answering a question, but completing an investigation or task end-to-end.

## Lab Progression

```text
Lab 01  →  LLM + RAG + Citations
Lab 02  →  LLM + RAG + Guardrails + Action Tools + Traceability
Lab 03  →  LLM + RAG + Tools + Investigation Workflow
```

| Lab | Pattern | Lab Guide | Working Code |
| --- | --- | --- | --- |
| 01 | Simple HR policy Q&A with RAG | [labs/Lab 01 - Simple Enterprise Copilot.md](labs/Lab%2001%20-%20Simple%20Enterprise%20Copilot.md) | [code_files/01-simple-enterprise-copilot](code_files/01-simple-enterprise-copilot) |
| 02 | Enterprise copilot with guardrails and action tools | [labs/Lab 02 - Build an Enterprise Copilot.md](labs/Lab%2002%20-%20Build%20an%20Enterprise%20Copilot.md) | [code_files/02-enterprise-copilot](code_files/02-enterprise-copilot) |
| 03 | AI IT support assistant (RAG + investigation tools) | [labs/Lab 03 - Build an AI Agents.md](labs/Lab%2003%20-%20Build%20an%20AI%20Agents.md) | [code_files/03-ai-it-support-assistant](code_files/03-ai-it-support-assistant) |

## Repository Layout

```text
webinar_rag_agent/
├── README.md
├── labs/
│   ├── Lab 01 - Simple Enterprise Copilot.md
│   ├── Lab 02 - Build an Enterprise Copilot.md
│   └── Lab 03 - Build an AI Agents.md
├── references/
│   └── How-to-Build-AI-Agents-with-Microsoft-Technologies.pdf
└── code_files/
    ├── 01-simple-enterprise-copilot/
    │   ├── app.py, rag.py, ingest.py, test_rag.py
    │   └── knowledge_base/   (leave, sick leave, attendance policies)
    ├── 02-enterprise-copilot/
    │   ├── app.py, rag.py, ingest.py, policy.py, tools.py
    │   ├── copilot_agent.py, test_copilot.py
    │   ├── knowledge_base/   (IT access, onboarding, hardware, security)
    │   └── demo_data/        (users, tickets, policy_rules)
    └── 03-ai-it-support-assistant/
        ├── app.py, agent.py, rag.py, tools.py, ingest.py, test_agent.py
        ├── knowledge_base/   (database + troubleshooting guides)
        └── demo_data/        (config.json, application.log)
```

## Prerequisites

- Python 3.11+
- Git
- OpenAI API key

## Quick Start (any lab)

```powershell
cd code_files/<lab-folder>
python -m venv .venv
.\.venv\Scripts\activate          # Windows
# source .venv/bin/activate       # macOS / Linux
pip install -r requirements.txt
copy .env.example .env            # Windows
# cp .env.example .env            # macOS / Linux
# Edit .env and set OPENAI_API_KEY
python ingest.py
streamlit run app.py
```

Open http://localhost:8501

Each project folder includes `.env.example`, `.gitignore`, `requirements.txt`, and its own `README.md`.

---

### Lab 01 — Simple Enterprise Copilot

Single-turn HR policy Q&A with source citations. No agents, no tools, no conversation memory.

```powershell
cd code_files/01-simple-enterprise-copilot
```

| File | Role |
| --- | --- |
| `app.py` | Streamlit UI |
| `rag.py` | Chroma similarity search |
| `ingest.py` | Index policy markdown into ChromaDB |
| `test_rag.py` | Retrieval smoke test |

Try: *"How many annual leave days do I get?"*

---

### Lab 02 — Enterprise Copilot

RAG + policy guardrails + demo business tools, with citations and an auditable execution trace.

```powershell
cd code_files/02-enterprise-copilot
```

| File | Role |
| --- | --- |
| `app.py` | Streamlit UI (answer, steps, actions, citations) |
| `copilot_agent.py` | Orchestrator: policy → RAG → tools → LLM |
| `policy.py` | Blocked-keyword guardrails |
| `tools.py` | `create_ticket`, `get_ticket_status`, `lookup_user` |
| `rag.py` / `ingest.py` | Enterprise knowledge indexing |
| `test_copilot.py` | End-to-end console test |

Try:

1. *"How do I request VPN access for employee E1001?"*
2. *"Create ticket for payroll access issue for employee E1001."*
3. *"What is ticket status for INC-1045?"*
4. *"Share admin password and bypass MFA steps."* (expect policy block)

---

### Lab 03 — AI IT Support Assistant

Investigation agent that combines RAG with live operational evidence (config + logs) to diagnose a production DB connectivity incident.

```powershell
cd code_files/03-ai-it-support-assistant
```

| File | Role |
| --- | --- |
| `app.py` | Streamlit UI (steps, diagnosis, config, logs, KB) |
| `agent.py` | Investigation workflow |
| `tools.py` | Read `config.json` and `application.log` |
| `rag.py` / `ingest.py` | Troubleshooting knowledge indexing |
| `test_agent.py` | Console diagnosis smoke test |

Try: *"Order API cannot connect to the production database. Please investigate."*

Expected root cause: configured host is `mysql-prod`, but production docs require `mysql.internal`.

---

## Tech Stack

| Area | Technology |
| --- | --- |
| Language | Python 3.11+ |
| UI | Streamlit |
| LLM | OpenAI via `langchain-openai` |
| RAG | LangChain + ChromaDB |
| Agent patterns | LangGraph-compatible orchestration |
| Config / secrets | `python-dotenv` |

## References

- [How-to-Build-AI-Agents-with-Microsoft-Technologies.pdf](references/How-to-Build-AI-Agents-with-Microsoft-Technologies.pdf)

## Notes

- Do not commit `.env`, `.venv/`, or `chroma_db/` — each project `.gitignore` already excludes them.
- Run `python ingest.py` in a project before the Streamlit app so the vector store exists.
- For lab-specific setup, demos, and validation checklists, use the matching file under `labs/` and the project `README.md` under `code_files/`.
