import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.models.document import Document
from app.schemas.document import DocumentListItem, DocumentResponse, PaginatedDocuments

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("", response_model=PaginatedDocuments)
async def list_documents(
    source_id: uuid.UUID | None = Query(None),
    doc_type: str | None = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> PaginatedDocuments:
    stmt = select(Document)
    count_stmt = select(func.count(Document.id))

    if source_id:
        stmt = stmt.where(Document.source_id == source_id)
        count_stmt = count_stmt.where(Document.source_id == source_id)
    if doc_type:
        stmt = stmt.where(Document.doc_type == doc_type)
        count_stmt = count_stmt.where(Document.doc_type == doc_type)

    total = (await db.execute(count_stmt)).scalar_one()
    offset = (page - 1) * size
    stmt = stmt.order_by(Document.created_at.desc()).offset(offset).limit(size)
    result = await db.execute(stmt)
    documents = result.scalars().all()

    return PaginatedDocuments(
        items=[DocumentListItem.model_validate(d) for d in documents],
        total=total,
        page=page,
        size=size,
    )


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> Document:
    doc: Document | None = await db.get(Document, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@router.delete("/{document_id}", status_code=204)
async def delete_document(
    document_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> None:
    doc = await db.get(Document, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    await db.delete(doc)
