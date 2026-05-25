from dataclasses import dataclass

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import CHUNK_OVERLAP, CHUNK_SIZE
from app.cv_ingestion.cv_text_extractor import CvPage


@dataclass(frozen=True)
class CvChunk:
    id: str
    text: str
    candidate_name: str
    filename: str
    page_number: int
    chunk_index: int


def chunk_cv_pages(pages: list[CvPage]) -> list[CvChunk]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks: list[CvChunk] = []
    for page in pages:
        page_chunks = splitter.split_text(page.text)
        for chunk_index, chunk_text in enumerate(page_chunks):
            chunks.append(
                CvChunk(
                    id=f"{page.filename}:p{page.page_number}:c{chunk_index}",
                    text=chunk_text,
                    candidate_name=page.candidate_name,
                    filename=page.filename,
                    page_number=page.page_number,
                    chunk_index=chunk_index,
                )
            )
    return chunks
