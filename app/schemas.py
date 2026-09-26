from datetime import datetime

from pydantic import BaseModel, Field


class DocumentInfo(BaseModel):
    id: str
    filename: str
    content_type: str | None = None
    chunks: int
    uploaded_at: datetime


class Source(BaseModel):
    document_id: str
    filename: str
    page: int | None = None
    chunk_index: int
    excerpt: str
    relevance: float = Field(ge=0, le=1)


class AskRequest(BaseModel):
    question: str = Field(min_length=2, max_length=4000)
    document_ids: list[str] | None = None
    top_k: int | None = Field(default=None, ge=1, le=10)


class AskResponse(BaseModel):
    answer: str
    sources: list[Source]


class UploadResponse(BaseModel):
    document: DocumentInfo
