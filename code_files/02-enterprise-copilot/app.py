"""Streamlit UI for the Enterprise Copilot."""

from __future__ import annotations

import os

import streamlit as st
from dotenv import load_dotenv

from copilot_agent import run_enterprise_copilot
from rag import BASE_DIR

load_dotenv(BASE_DIR / ".env")

st.set_page_config(page_title="Enterprise Copilot", page_icon="🏢")
st.title("Enterprise Copilot")
st.caption("RAG + Guardrails + Action Tools")

_api_key = os.getenv("OPENAI_API_KEY", "").strip()
if not _api_key or _api_key == "your-openai-api-key":
    st.error(
        "OPENAI_API_KEY is not set. Copy `.env.example` to `.env` and add your key."
    )
    st.stop()

prompt = st.text_area(
    "Ask a question or request an action",
    value="How do I request VPN access for employee E1001?",
    height=120,
)

if st.button("Run Copilot", type="primary"):
    if not prompt.strip():
        st.warning("Please enter a question or action request.")
    else:
        with st.spinner("Processing request..."):
            result = run_enterprise_copilot(prompt)

        st.subheader("Copilot Response")
        st.write(result["answer"])

        st.subheader("Execution Steps")
        for step in result["steps"]:
            st.success(step)

        with st.expander("Actions", expanded=bool(result["actions"])):
            st.json(result["actions"])

        with st.expander("Citations", expanded=True):
            if result["citations"]:
                for item in result["citations"]:
                    st.write(f"- {item}")
            else:
                st.write("No citations retrieved.")
