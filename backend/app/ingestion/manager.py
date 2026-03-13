import hashlib
import logging
import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ingestion.base import BaseIngestor, IngestedDocument
from app.ingestion.document_ingestor import DocumentIngestor
from app.ingestion.email_ingestor import EmailIngestor
from app.ingestion.github_ingestor import GitHubIngestor
from app.ingestion.markdown_ingestor import MarkdownIngestor
from app.models.document import Document, DocumentChunk
from app.models.job import IngestionJob
from app.models.source import DataSource
from app.services.chunker import TextChunker
from app.services.embedding import EmbeddingService

logger = logging.getLogger(__name__)

INGESTOR_MAP: dict[str, type[BaseIngestor]] = {
    "github": GitHubIngestor,
    "email": EmailIngestor,
    "document": DocumentIngestor,
    "markdown": MarkdownIngestor,
}


class IngestionManager:
    def __init__(
        self,
        db: AsyncSession,
        embedding_service: EmbeddingService,
        chunker: TextChunker | None = None,
    ) -> None:
        self.db = db
        self.embedding_service = embedding_service
        self.chunker = chunker or TextChunker()

    async def run(self, source_id: uuid.UUID, job_id: uuid.UUID) -> None:
        job = await self.db.get(IngestionJob, job_id)
        source = await self.db.get(DataSource, source_id)
        if not job or not source:
            logger.error("Job %s or source %s not found", job_id, source_id)
            return

        job.status = "running"
        job.started_at = datetime.now(timezone.utc)
        await self.db.commit()

        try:
            ingestor_cls = INGESTOR_MAP.get(source.source_type)
            if not ingestor_cls:
                raise ValueError(f"Unknown source type: {source.source_type}")

            ingestor = ingestor_cls()
            if not await ingestor.validate_config(source.config):
                raise ValueError(f"Invalid config for source {source.name}")

            raw_documents = await ingestor.ingest(source.config)
            job.documents_total = len(raw_documents)
            await self.db.commit()

            total_chunks = 0
            for ingested_doc in raw_documents:
                chunks_created = await self._process_document(source.id, ingested_doc)
                total_chunks += chunks_created
                job.documents_processed += 1
                job.chunks_created = total_chunks
                await self.db.commit()

            source.document_count = job.documents_processed
            source.last_synced_at = datetime.now(timezone.utc)
            job.status = "completed"
            job.completed_at = datetime.now(timezone.utc)
            await self.db.commit()

        except Exception as e:
            logger.exception("Ingestion failed for job %s", job_id)
            job.status = "failed"
            job.error_message = str(e)
            job.completed_at = datetime.now(timezone.utc)
            await self.db.commit()

    async def _process_document(
        self, source_id: uuid.UUID, ingested: IngestedDocument
    ) -> int:
        content_hash = hashlib.sha256(ingested.content.encode()).hexdigest()

        # Check for existing document (dedup)
        existing = await self.db.execute(
            select(Document).where(
                Document.source_id == source_id,
                Document.external_id == ingested.external_id,
            )
        )
        doc = existing.scalar_one_or_none()

        if doc and doc.content_hash == content_hash:
            return 0  # No change

        if doc:
            # Update existing: delete old chunks, update content
            for chunk in doc.chunks:
                await self.db.delete(chunk)
            doc.content = ingested.content
            doc.title = ingested.title
            doc.metadata_ = ingested.metadata
            doc.content_hash = content_hash
        else:
            doc = Document(
                source_id=source_id,
                external_id=ingested.external_id,
                title=ingested.title,
                doc_type=ingested.doc_type,
                content=ingested.content,
                metadata_=ingested.metadata,
                content_hash=content_hash,
            )
            self.db.add(doc)
            await self.db.flush()

        # Chunk and embed
        text_chunks = self.chunker.chunk_text(ingested.content)
        if not text_chunks:
            return 0

        texts = [c.content for c in text_chunks]
        embeddings = self.embedding_service.embed_batch(texts)

        for chunk, embedding in zip(text_chunks, embeddings):
            db_chunk = DocumentChunk(
                document_id=doc.id,
                chunk_index=chunk.chunk_index,
                content=chunk.content,
                token_count=chunk.token_count,
                embedding=embedding,
            )
            self.db.add(db_chunk)

        return len(text_chunks)
