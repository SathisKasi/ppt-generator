import re

from app.models.document_model import Knowledge, NormalizedDocument


def analyze(document: NormalizedDocument) -> Knowledge:
    lines = [line.strip() for line in document.text.splitlines() if line.strip()]
    subject = next((line.lstrip("# ").strip() for line in lines if line.startswith("#")), lines[0] if lines else "Not provided")[:120]
    problem = next((line for line in lines if any(word in line.lower() for word in ("problem", "challenge", "issue"))), "Not provided")
    objectives = [line for line in lines if any(word in line.lower() for word in ("objective", "goal", "target"))][:5]
    numbers = re.findall(r"\b\d+(?:\.\d+)?%?\b", document.text)
    dates = re.findall(r"\b(?:20\d{2}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b", document.text)
    sections = []
    current = None
    for line in document.text.splitlines():
        text = line.strip()
        if text.startswith("## "):
            if current is not None:
                sections.append(current)
            current = {"title": re.sub(r"^\d+[.)]?\s*", "", text[3:]).strip(), "lines": []}
        elif current is not None and text and not text.startswith("---"):
            current["lines"].append(text.lstrip("*- ").strip())
    if current is not None:
        sections.append(current)
    return Knowledge(
        subject=subject,
        problem=problem,
        objectives=objectives,
        sections=sections,
        facts=lines[:10],
        numbers=numbers,
        dates=dates,
        conclusions=lines[-3:],
        source_references=[document.file_name],
    )