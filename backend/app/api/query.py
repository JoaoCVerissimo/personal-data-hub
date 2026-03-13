from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.schemas.query import QueryRequest, SearchResponse, SearchResultItem
from app.services.embedding import get_embedding_service
from app.services.search import SearchService

router = APIRouter(prefix="/query", tags=["query"])


@router.post("/search", response_model=SearchResponse)
async def search(
    payload: QueryRequest,
    db: AsyncSession = Depends(get_db),
) -> SearchResponse:
    embedding_service = get_embedding_service()
    search_service = SearchService(db=db, embedding_service=embedding_service)

    filters = payload.filters
    result = await search_service.search(
        query=payload.query,
        limit=payload.limit,
        source_types=filters.source_types if filters else None,
        source_ids=filters.source_ids if filters else None,
        doc_types=filters.doc_types if filters else None,
    )

    return SearchResponse(
        results=[
            SearchResultItem(
                chunk_id=r.chunk_id,
                document_id=r.document_id,
                document_title=r.document_title,
                source_name=r.source_name,
                source_type=r.source_type,
                content=r.content,
                score=r.score,
                metadata=r.metadata,
                source_config=r.source_config,
            )
            for r in result.results
        ],
        total=result.total,
        query_time_ms=result.query_time_ms,
    )
