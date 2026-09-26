from __future__ import annotations

import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.documents import SUPPORTED_EXTENSIONS, chunk_text, extract_pages
from app.qa import answer_question
from app.schemas import AskRequest, AskResponse, DocumentInfo, Source, UploadResponse
from app.store import registry, vector_store

app = FastAPI(title=settings.app_name, version="1.0.0")
app.add_middleware(
    CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/documents", response_model=list[DocumentInfo])
def list_documents() -> list[DocumentInfo]:
    return registry.list()


@app.post("/documents", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
def upload_document(file: UploadFile = File(...)) -> UploadResponse:
    filename = Path(file.filename or "document").name
    suffix = Path(filename).suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise HTTPException(415, f"Unsupported type. Use one of: {', '.join(sorted(SUPPORTED_EXTENSIONS))}")

    document_id = str(uuid4())
    saved_path = settings.upload_dir / f"{document_id}{suffix}"
    try:
        with saved_path.open("wb") as destination:
            shutil.copyfileobj(file.file, destination)
        pages = extract_pages(saved_path)
        texts: list[str] = []
        ids: list[str] = []
        metadata: list[dict] = []
        for page_data in pages:
            for text in chunk_text(page_data.text, settings.chunk_size, settings.chunk_overlap):
                index = len(texts)
                texts.append(text)
                ids.append(f"{document_id}:{index}")
                metadata.append({"document_id": document_id, "filename": filename, "page": page_data.page or -1, "chunk_index": index})
        if not texts:
            raise HTTPException(422, "No readable text was found in this document.")
        vector_store.add(ids, texts, metadata)
        document = registry.add(document_id=document_id, filename=filename, content_type=file.content_type, chunks=len(texts))
        return UploadResponse(document=document)
    except HTTPException:
        saved_path.unlink(missing_ok=True)
        raise
    except Exception as exc:
        vector_store.delete_document(document_id)
        saved_path.unlink(missing_ok=True)
        raise HTTPException(500, f"Indexing failed: {exc}") from exc
    finally:
        file.file.close()


@app.delete("/documents/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(document_id: str) -> None:
    document = registry.delete(document_id)
    if not document:
        raise HTTPException(404, "Document not found")
    vector_store.delete_document(document_id)
    for file_path in settings.upload_dir.glob(f"{document_id}.*"):
        file_path.unlink(missing_ok=True)


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    try:
        chunks = vector_store.query(request.question, request.top_k or settings.top_k, request.document_ids)
    except Exception as exc:
        raise HTTPException(500, f"Retrieval failed: {exc}") from exc
    try:
        answer = answer_question(request.question, chunks)
    except (RuntimeError, ValueError) as exc:
        raise HTTPException(503, str(exc)) from exc
    except Exception as exc:
        raise HTTPException(502, f"Answer generation failed: {exc}") from exc
    sources = [
        Source(
            document_id=item["metadata"]["document_id"], filename=item["metadata"]["filename"],
            page=None if item["metadata"].get("page", -1) == -1 else item["metadata"]["page"],
            chunk_index=item["metadata"]["chunk_index"], excerpt=item["text"][:350],
            relevance=max(0.0, min(1.0, 1.0 - item["distance"])),
        )
        for item in chunks
    ]
    return AskResponse(answer=answer, sources=sources)
