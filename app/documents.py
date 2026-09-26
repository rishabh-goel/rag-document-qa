"""Document parsing and deterministic, overlap-aware chunking."""

from __future__ import annotations

import csv
import io
from dataclasses import dataclass
from pathlib import Path

import fitz
from docx import Document


SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt", ".md", ".csv"}


@dataclass(frozen=True)
class PageText:
    text: str
    page: int | None


def extract_pages(path: Path) -> list[PageText]:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        with fitz.open(path) as pdf:
            return [PageText(page.get_text("text"), i + 1) for i, page in enumerate(pdf)]
    if suffix == ".docx":
        document = Document(path)
        return [PageText("\n".join(p.text for p in document.paragraphs), None)]
    if suffix in {".txt", ".md"}:
        return [PageText(path.read_text(encoding="utf-8", errors="replace"), None)]
    if suffix == ".csv":
        with path.open("r", encoding="utf-8", errors="replace", newline="") as file:
            rows = csv.reader(file)
            return [PageText("\n".join(" | ".join(row) for row in rows), None)]
    raise ValueError(f"Unsupported file type: {suffix}")


def normalize(text: str) -> str:
    return " ".join(text.replace("\x00", " ").split())


def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Split text near sentence/word boundaries, retaining a character overlap."""
    text = normalize(text)
    if not text:
        return []
    if overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end < len(text):
            boundary = max(text.rfind(". ", start, end), text.rfind(" ", start, end))
            if boundary > start + (chunk_size // 2):
                end = boundary + 1
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(text):
            break
        start = max(end - overlap, start + 1)
    return chunks
