import time
import uuid
from dataclasses import dataclass

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document, DocumentChunk
from app.models.source import DataSource
from app.models.query_log import QueryLog
from app.services.embedding import EmbeddingService


@dataclass
class SearchResult:
    chunk_id: uuid.UUID
    document_id: uuid.UUID
    document_title: str | None
    source_name: str
    source_type: str
    content: str
    score: float
    metadata: dict


@dataclass
class SearchResponse:
    results: list[SearchResult]
    total: int
    query_time_ms: int


class SearchService:
    def __init__(self, db: AsyncSession, embedding_service: EmbeddingService) -> None:
        self.db = db
        self.embedding_service = embedding_service

    async def search(
        self,
        query: str,
        limit: int = 20,
        source_types: list[str] | None = None,
        source_ids: list[uuid.UUID] | None = None,
        doc_types: list[str] | None = None,
    ) -> SearchResponse:
        start = time.monotonic()

        query_embedding = self.embedding_service.embed_text(query)
        embedding_str = "[" + ",".join(str(v) for v in query_embedding) + "]"

        stmt = (
            select(
                DocumentChunk.id,
                DocumentChunk.document_id,
                DocumentChunk.content,
                Document.title,
                Document.metadata_.label("doc_metadata"),
                DataSource.name.label("source_name"),
                DataSource.source_type,
                DocumentChunk.embedding.cosine_distance(query_embedding).label("distance"),
            )
            .join(Document, DocumentChunk.document_id == Document.id)
            .join(DataSource, Document.source_id == DataSource.id)
        )

        if source_types:
            stmt = stmt.where(DataSource.source_type.in_(source_types))
        if source_ids:
            stmt = stmt.where(DataSource.id.in_(source_ids))
        if doc_types:
            stmt = stmt.where(Document.doc_type.in_(doc_types))

        stmt = stmt.order_by("distance").limit(limit)

        result = await self.db.execute(stmt)
        rows = result.all()

        results = [
            SearchResult(
                chunk_id=row.id,
                document_id=row.document_id,
                document_title=row.title,
                source_name=row.source_name,
                source_type=row.source_type,
                content=row.content,
                score=round(1 - row.distance, 4),
                metadata=row.doc_metadata or {},
            )
            for row in rows
        ]

        elapsed_ms = int((time.monotonic() - start) * 1000)

        log_entry = QueryLog(
            query_text=query,
            result_count=len(results),
            latency_ms=elapsed_ms,
            filters={
                "source_types": source_types,
                "source_ids": [str(s) for s in source_ids] if source_ids else None,
                "doc_types": doc_types,
            },
        )
        self.db.add(log_entry)

        return SearchResponse(results=results, total=len(results), query_time_ms=elapsed_ms)
