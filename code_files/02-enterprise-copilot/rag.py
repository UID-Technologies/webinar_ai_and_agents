"""RAG utilities for the Enterprise Copilot."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
CHROMA_DIR = str(BASE_DIR / "chroma_db")
COLLECTION_NAME = "enterprise_knowledge"


def get_vector_store() -> Chroma:
    """Return the persistent Chroma vector store for enterprise knowledge."""
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )


def search_knowledge(query: str, k: int = 4):
    """Retrieve the top-k knowledge chunks most similar to the query."""
    return get_vector_store().similarity_search(query, k=k)
