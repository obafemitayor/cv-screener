import asyncio
import logging

from app.cv_ingestion.chunker import chunk_cv_pages
from app.cv_ingestion.cv_text_extractor import extract_text_from_cvs
from app.utils.embeddings import generate_embedding_from_text
from app.config import CV_PDF_DIR
from app.storage.vector_store import reset_collection, upsert_chunks

logger = logging.getLogger(__name__)
EMBEDDING_REQUEST_DELAY_SECONDS = 0.75


async def ingest_cvs() -> dict[str, int]:
    logger.info("Starting CV ingestion from %s", CV_PDF_DIR)
    pages = extract_text_from_cvs(CV_PDF_DIR)
    logger.info("Extracted %s pages from CV PDFs", len(pages))

    chunks = chunk_cv_pages(pages)
    logger.info("Chunked CV text into %s chunks", len(chunks))

    embeddings = []
    for index, chunk in enumerate(chunks, start=1):
        embeddings.append(
            await generate_embedding_from_text(
                chunk.text,
                task_type="RETRIEVAL_DOCUMENT",
            )
        )
        if index < len(chunks):
            await asyncio.sleep(EMBEDDING_REQUEST_DELAY_SECONDS)

    logger.info("Resetting Chroma collection")
    reset_collection()
    logger.info("Writing %s chunks to Chroma", len(chunks))
    upsert_chunks(chunks, embeddings)
    logger.info("CV ingestion finished successfully")

    return {
        "pdf_pages": len(pages),
        "chunks": len(chunks),
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    result = asyncio.run(ingest_cvs())
    print(f"Ingested {result['pdf_pages']} PDF pages into {result['chunks']} chunks.")
