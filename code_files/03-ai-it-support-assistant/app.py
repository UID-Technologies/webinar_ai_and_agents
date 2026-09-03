"""Streamlit UI for the AI IT Support Assistant."""

from __future__ import annotations

import os

import streamlit as st
from dotenv import load_dotenv

from agent import investigate_incident
from rag import BASE_DIR

load_dotenv(BASE_DIR / ".env")

st.set_page_config(page_title="AI IT Support Assistant", page_icon="🔧")
st.title("AI IT Support Assistant")
st.caption("RAG + Tools + Agent Workflow")

_api_key = os.getenv("OPENAI_API_KEY", "").strip()
if not _api_key or _api_key == "your-openai-api-key":
    st.error(
        "OPENAI_API_KEY is not set. Copy `.env.example` to `.env` and add your key."
    )
    st.stop()

issue = st.text_area(
    "Describe your support problem",
    value="Order API cannot connect to the production database. Please investigate.",
    height=120,
)

if st.button("Investigate", type="primary"):
    if not issue.strip():
        st.warning("Please describe the incident.")
    else:
        with st.spinner("Investigating incident..."):
            result = investigate_incident(issue)

        st.subheader("Agent Activity")
        for step in result["steps"]:
            st.success(step)

        st.subheader("AI Diagnosis")
        st.write(result["answer"])

        with st.expander("Application Configuration"):
            st.json(result["config"])

        with st.expander("Application Logs"):
            st.code(result["logs"])

        with st.expander("Retrieved Knowledge"):
            for document in result["documents"]:
                source = document.metadata.get("source", "Unknown")
                st.write(f"**Source:** {source}")
                st.write(document.page_content)
                st.divider()
