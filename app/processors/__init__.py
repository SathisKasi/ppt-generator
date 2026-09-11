from pathlib import Path
from typing import Callable

from app.models.document_model import NormalizedDocument


Processor = Callable[[Path, str], NormalizedDocument]


def supported_extensions() -> set[str]:
    return {".pdf", ".docx", ".pptx", ".xlsx", ".csv", ".txt", ".md", ".markdown"}


def extract_document(path: Path, original_name: str) -> NormalizedDocument:
    from app.processors.document_processor import extract_document as extract

    return extract(path, original_name)