from pathlib import Path

import pytest

from app.processors.document_processor import extract_document


def test_text_extraction(tmp_path: Path):
    source = tmp_path / "notes.txt"
    source.write_text("Important business context", encoding="utf-8")
    document = extract_document(source, "notes.txt")
    assert document.text == "Important business context"
    assert document.file_type == "txt"


def test_unsupported_file_is_clear(tmp_path: Path):
    source = tmp_path / "script.exe"
    source.write_bytes(b"not executable")
    with pytest.raises(ValueError, match="Unsupported file type"):
        extract_document(source, source.name)