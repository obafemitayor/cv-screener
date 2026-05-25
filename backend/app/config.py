import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")


def _path_from_env(name: str, default: str) -> Path:
    path = Path(os.getenv(name, default))
    if not path.is_absolute():
        path = BASE_DIR / path
    return path


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GEMINI_EMBEDDING_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL", "gemini-embedding-001")
GEMINI_CHAT_MODEL = os.getenv("GEMINI_CHAT_MODEL", "gemini-2.5-flash")

CV_PDF_DIR = _path_from_env("CV_PDF_DIR", "data/cvs")
CHROMA_DIR = _path_from_env("CHROMA_DIR", "data/chroma")
CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION", "cv_chunks")

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1100"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "180"))

CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ALLOWED_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]

CV_HISTORY_MAX_TURNS = int(os.getenv("CV_HISTORY_MAX_TURNS", "8"))
CV_HISTORY_MAX_CHARS = int(os.getenv("CV_HISTORY_MAX_CHARS", "4000"))
