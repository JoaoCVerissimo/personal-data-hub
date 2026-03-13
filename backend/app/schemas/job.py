from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class JobCreate(BaseModel):
    job_type: str = "full"


class JobResponse(BaseModel):
    id: UUID
    source_id: UUID
    status: str
    job_type: str
    documents_total: int
    documents_processed: int
    chunks_created: int
    error_message: str | None
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}
