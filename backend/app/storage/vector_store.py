import logging
from typing import Any

import chromadb
from chromadb.config import Settings

from app.cv_ingestion.chunker import CvChunk
from app.config import CHROMA_COLLECTION, CHROMA_DIR

logging.getLogger("chromadb.telemetry.product.posthog").setLevel(logging.CRITICAL)


def get_collection() -> Any:
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = _client()
    return client.get_or_create_collection(
        name=CHROMA_COLLECTION,
        metadata={"hnsw:space": "cosine"},
    )


def reset_collection() -> Any:
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = _client()
    try:
        client.delete_collection(CHROMA_COLLECTION)
    except ValueError:
        pass
    return client.get_or_create_collection(
        name=CHROMA_COLLECTION,
        metadata={"hnsw:space": "cosine"},
    )


def _client() -> Any:
    return chromadb.PersistentClient(
        path=str(CHROMA_DIR),
        settings=Settings(anonymized_telemetry=False),
    )


def upsert_chunks(chunks: list[CvChunk], embeddings: list[list[float]]) -> None:
    if not chunks:
        return

    collection = get_collection()
    collection.upsert(
        ids=[chunk.id for chunk in chunks],
        documents=[chunk.text for chunk in chunks],
        embeddings=embeddings,
        metadatas=[
            {
                "candidate_name": chunk.candidate_name,
                "filename": chunk.filename,
                "page_number": chunk.page_number,
                "chunk_index": chunk.chunk_index,
            }
            for chunk in chunks
        ],
    )


def delete_cv_chunks(filename: str) -> None:
    collection = get_collection()
    collection.delete(where={"filename": filename})


def get_cvs_similar_to_embedding(
    embedding: list[float],
    top_k: int,
) -> list[dict[str, Any]]:
    collection = get_collection()
    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    matches: list[dict[str, Any]] = []
    for index, document in enumerate(results.get("documents", [[]])[0]):
        metadata = results.get("metadatas", [[]])[0][index]
        distance = results.get("distances", [[]])[0][index]
        matches.append(
            {
                "text": document,
                "metadata": metadata,
                "distance": distance,
            }
        )
    return matches
