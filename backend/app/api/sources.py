import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.models.job import IngestionJob
from app.models.source import DataSource
from app.schemas.job import JobCreate, JobResponse
from app.schemas.source import SourceCreate, SourceResponse, SourceUpdate
from app.worker.queue import get_queue
from app.worker.tasks import run_ingestion

router = APIRouter(prefix="/sources", tags=["sources"])


@router.get("", response_model=list[SourceResponse])
async def list_sources(db: AsyncSession = Depends(get_db)) -> list[DataSource]:
    result = await db.execute(select(DataSource).order_by(DataSource.created_at.desc()))
    return list(result.scalars().all())


@router.post("", response_model=SourceResponse, status_code=201)
async def create_source(
    payload: SourceCreate, db: AsyncSession = Depends(get_db)
) -> DataSource:
    source = DataSource(
        name=payload.name,
        source_type=payload.source_type,
        config=payload.config,
    )
    db.add(source)
    await db.flush()
    await db.refresh(source)
    return source


@router.get("/{source_id}", response_model=SourceResponse)
async def get_source(
    source_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> DataSource:
    source = await db.get(DataSource, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


@router.put("/{source_id}", response_model=SourceResponse)
async def update_source(
    source_id: uuid.UUID,
    payload: SourceUpdate,
    db: AsyncSession = Depends(get_db),
) -> DataSource:
    source = await db.get(DataSource, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    if payload.name is not None:
        source.name = payload.name
    if payload.config is not None:
        source.config = payload.config
    if payload.status is not None:
        source.status = payload.status
    await db.flush()
    await db.refresh(source)
    return source


@router.delete("/{source_id}", status_code=204)
async def delete_source(
    source_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> None:
    source = await db.get(DataSource, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    await db.delete(source)


@router.post("/{source_id}/sync", response_model=JobResponse)
async def sync_source(
    source_id: uuid.UUID,
    payload: JobCreate = JobCreate(),
    db: AsyncSession = Depends(get_db),
) -> IngestionJob:
    source = await db.get(DataSource, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    job = IngestionJob(source_id=source_id, job_type=payload.job_type)
    db.add(job)
    await db.flush()
    await db.refresh(job)

    queue = get_queue()
    queue.enqueue(run_ingestion, str(source_id), str(job.id))

    return job
