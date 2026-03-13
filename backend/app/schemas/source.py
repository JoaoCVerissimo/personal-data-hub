from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SourceCreate(BaseModel):
    name: str
    source_type: str
    config: dict = {}


class SourceUpdate(BaseModel):
    name: str | None = None
    config: dict | None = None
    status: str | None = None


class SourceResponse(BaseModel):
    id: UUID
    name: str
    source_type: str
    config: dict
    status: str
    document_count: int
    last_synced_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
