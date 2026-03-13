from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: UUID
    source_id: UUID
    external_id: str | None
    title: str | None
    doc_type: str
    content: str
    metadata: dict
    content_hash: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class DocumentListItem(BaseModel):
    id: UUID
    source_id: UUID
    title: str | None
    doc_type: str
    content_hash: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class PaginatedDocuments(BaseModel):
    items: list[DocumentListItem]
    total: int
    page: int
    size: int
