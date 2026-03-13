from uuid import UUID

from pydantic import BaseModel


class QueryFilters(BaseModel):
    source_types: list[str] | None = None
    source_ids: list[UUID] | None = None
    doc_types: list[str] | None = None


class QueryRequest(BaseModel):
    query: str
    filters: QueryFilters | None = None
    limit: int = 20


class SearchResultItem(BaseModel):
    chunk_id: UUID
    document_id: UUID
    document_title: str | None
    source_name: str
    source_type: str
    content: str
    score: float
    metadata: dict


class SearchResponse(BaseModel):
    results: list[SearchResultItem]
    total: int
    query_time_ms: int
