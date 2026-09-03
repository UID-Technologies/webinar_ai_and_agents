# Lab 03 — AI IT Support Assistant

Agent-driven IT incident investigation using RAG + operational tools + LLM reasoning.

## Architecture

```text
User Incident → Streamlit UI → AI Investigation Agent
                                    ├── RAG Search (ChromaDB)
                                    ├── Config Tool (config.json)
                                    ├── Logs Tool (application.log)
                                    └── LLM → Diagnosis + Recommendation
```

## Prerequisites

- Python 3.11+
- OpenAI API key

## Setup

```bash
cd code_files/03-ai-it-support-assistant
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

## Console test

```bash
python test_agent.py
```

## Demo scenario

The Order API uses `DB_HOST=mysql-prod` but production docs say `mysql.internal`.
The agent should identify this hostname mismatch as the root cause.

## Demo variations

- **Port mismatch:** change `DB_PORT` to `3307` in `demo_data/config.json`
- **Expanded KB:** add `knowledge_base/network_guide.md` and re-run ingest

## Project layout

```text
03-ai-it-support-assistant/
├── app.py
├── agent.py
├── rag.py
├── tools.py
├── ingest.py
├── test_agent.py
├── knowledge_base/
├── demo_data/
├── chroma_db/          # created by ingest.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```
