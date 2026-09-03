"""Ingest enterprise knowledge documents into the Chroma vector store."""

from __future__ import annotations

import os
import shutil
from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag import BASE_DIR, CHROMA_DIR, COLLECTION_NAME, get_vector_store

KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"


def load_documents():
    """Load all markdown knowledge files from the knowledge base."""
    documents = []
    policy_files = sorted(KNOWLEDGE_BASE_DIR.glob("*.md"))

    if not policy_files:
        raise FileNotFoundError(
            f"No markdown files found in {KNOWLEDGE_BASE_DIR}"
        )

    for file_path in policy_files:
        loader = TextLoader(str(file_path), encoding="utf-8")
        loaded = loader.load()
        for doc in loaded:
            doc.metadata["source"] = file_path.name
        documents.extend(loaded)

    return documents


def reset_vector_store() -> None:
    """Remove the persisted Chroma directory so re-ingest stays idempotent."""
    chroma_path = Path(CHROMA_DIR)
    if chroma_path.exists():
        shutil.rmtree(chroma_path)


def ingest() -> None:
    """Chunk knowledge documents and index them into ChromaDB."""
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key or api_key == "your-openai-api-key":
        raise EnvironmentError(
            "Set OPENAI_API_KEY in .env before running ingest. "
            "Copy .env.example to .env and add your key."
        )

    docs = load_documents()
    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=80)
    chunks = splitter.split_documents(docs)

    reset_vector_store()
    vector_store = get_vector_store()
    vector_store.add_documents(chunks)

    print(
        f"Enterprise knowledge base indexed successfully "
        f"({len(docs)} files, {len(chunks)} chunks) "
        f"into collection '{COLLECTION_NAME}'."
    )


if __name__ == "__main__":
    ingest()
