"""Persistent Chroma collection plus a small local document registry."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from app.config import settings
from app.schemas import DocumentInfo


class VectorStore:
    def __init__(self) -> None:
        self.client = chromadb.PersistentClient(path=str(settings.chroma_dir))
        embedder = SentenceTransformerEmbeddingFunction(model_name=settings.embedding_model)
        self.collection = self.client.get_or_create_collection(
            name="document_chunks", embedding_function=embedder, metadata={"hnsw:space": "cosine"}
        )

    def add(self, ids: list[str], texts: list[str], metadatas: list[dict]) -> None:
        self.collection.add(ids=ids, documents=texts, metadatas=metadatas)

    def query(self, question: str, top_k: int, document_ids: list[str] | None = None) -> list[dict]:
        where = {"document_id": {"$in": document_ids}} if document_ids else None
        result = self.collection.query(query_texts=[question], n_results=top_k, where=where)
        items: list[dict] = []
        for item_id, text, metadata, distance in zip(
            result["ids"][0], result["documents"][0], result["metadatas"][0], result["distances"][0]
        ):
            items.append({"id": item_id, "text": text, "metadata": metadata, "distance": float(distance)})
        return items

    def delete_document(self, document_id: str) -> None:
        found = self.collection.get(where={"document_id": document_id}, include=[])
        if found["ids"]:
            self.collection.delete(ids=found["ids"])


class DocumentRegistry:
    def __init__(self, path: Path) -> None:
        self.path = path

    def _read(self) -> list[dict]:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _write(self, documents: list[dict]) -> None:
        self.path.write_text(json.dumps(documents, indent=2), encoding="utf-8")

    def add(self, *, document_id: str, filename: str, content_type: str | None, chunks: int) -> DocumentInfo:
        record = DocumentInfo(
            id=document_id,
            filename=filename,
            content_type=content_type,
            chunks=chunks,
            uploaded_at=datetime.now(UTC),
        )
        documents = self._read()
        documents.append(record.model_dump(mode="json"))
        self._write(documents)
        return record

    def list(self) -> list[DocumentInfo]:
        return [DocumentInfo.model_validate(item) for item in self._read()]

    def delete(self, document_id: str) -> DocumentInfo | None:
        documents = self._read()
        remaining = [doc for doc in documents if doc["id"] != document_id]
        if len(remaining) == len(documents):
            return None
        removed = next(doc for doc in documents if doc["id"] == document_id)
        self._write(remaining)
        return DocumentInfo.model_validate(removed)


vector_store = VectorStore()
registry = DocumentRegistry(settings.registry_path)
