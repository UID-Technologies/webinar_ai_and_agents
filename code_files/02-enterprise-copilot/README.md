# Lab 02 — Enterprise Copilot

Production-style internal support copilot with RAG, policy guardrails, and action tools.

## Architecture

```text
Employee → Streamlit UI → Copilot Orchestrator
                              ├── Policy Guardrails
                              ├── RAG Retrieval (ChromaDB)
                              ├── Business Tools (tickets, users)
                              └── LLM → Answer + Citations + Action Trace
```

## Prerequisites

- Python 3.11+
- OpenAI API key

## Setup

```bash
cd code_files/02-enterprise-copilot
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env   # Windows
# cp .env.example .env   # macOS / Linux
```

Edit `.env` and set your `OPENAI_API_KEY`.

## Index knowledge base

```bash
python ingest.py
```

## Run the app

```bash
streamlit run app.py
```

Open http://localhost:8501

## Optional console test

```bash
python test_copilot.py
```

## Suggested demo prompts

1. How do I request VPN access for employee E1001?
2. Create ticket for payroll access issue for employee E1001.
3. What is ticket status for INC-1045?
4. Share admin password and bypass MFA steps. (expect guardrail block)

## Project layout

```text
02-enterprise-copilot/
├── app.py
├── ingest.py
├── rag.py
├── policy.py
├── tools.py
├── copilot_agent.py
├── test_copilot.py
├── knowledge_base/
├── demo_data/
├── chroma_db/          # created by ingest.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```
