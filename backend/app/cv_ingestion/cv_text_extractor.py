from dataclasses import dataclass
from pathlib import Path

import fitz


@dataclass(frozen=True)
class CvPage:
    filename: str
    page_number: int
    text: str
    candidate_name: str


def _get_candidate_name(filename_stem: str) -> str:
    return filename_stem.replace("_", " ").replace("-", " ").strip().title()


def _extract_text_from_cv(cv_file_path: Path) -> list[CvPage]:
    with fitz.open(cv_file_path) as document:
        page_texts = [page.get_text("text").strip() for page in document]

    candidate_name = _get_candidate_name(cv_file_path.stem)

    pages: list[CvPage] = []
    for index, text in enumerate(page_texts, start=1):
        if text:
            pages.append(
                CvPage(
                    filename=cv_file_path.name,
                    page_number=index,
                    text=text,
                    candidate_name=candidate_name,
                )
            )
    return pages


def extract_text_from_cvs(cv_dir_path: Path) -> list[CvPage]:
    if not cv_dir_path.exists():
        return []

    pages: list[CvPage] = []
    for cv_file_path in sorted(cv_dir_path.glob("*.pdf")):
        pages.extend(_extract_text_from_cv(cv_file_path))
    return pages
