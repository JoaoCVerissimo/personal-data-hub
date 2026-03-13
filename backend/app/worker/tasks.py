import asyncio
import uuid

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings
from app.ingestion.manager import IngestionManager
from app.services.embedding import get_embedding_service


def run_ingestion(source_id: str, job_id: str) -> None:
    """RQ task: runs the ingestion pipeline for a source."""
    asyncio.run(_run_ingestion_async(uuid.UUID(source_id), uuid.UUID(job_id)))


async def _run_ingestion_async(source_id: uuid.UUID, job_id: uuid.UUID) -> None:
    engine = create_async_engine(settings.database_url, echo=False)
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with session_factory() as session:
        embedding_service = get_embedding_service()
        manager = IngestionManager(db=session, embedding_service=embedding_service)
        await manager.run(source_id=source_id, job_id=job_id)

    await engine.dispose()
