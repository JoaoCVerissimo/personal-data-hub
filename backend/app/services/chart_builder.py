from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Interval, func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document
from app.models.job import IngestionJob
from app.models.query_log import QueryLog
from app.models.source import DataSource


@dataclass
class ChartDataPoint:
    label: str
    value: int


@dataclass
class TimeSeriesPoint:
    date: str
    value: int


class ChartBuilder:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def source_distribution(self) -> list[ChartDataPoint]:
        stmt = (
            select(DataSource.source_type, func.count(Document.id).label("count"))
            .outerjoin(Document, DataSource.id == Document.source_id)
            .group_by(DataSource.source_type)
            .order_by(func.count(Document.id).desc())
        )
        result = await self.db.execute(stmt)
        return [ChartDataPoint(label=row.source_type, value=row.count) for row in result.all()]

    async def ingestion_timeline(self, days: int = 30) -> list[TimeSeriesPoint]:
        stmt = (
            select(
                func.date_trunc("day", Document.created_at).label("day"),
                func.count(Document.id).label("count"),
            )
            .where(Document.created_at >= func.now() - text(f"interval '{days} days'"))
            .group_by("day")
            .order_by("day")
        )
        result = await self.db.execute(stmt)
        return [
            TimeSeriesPoint(date=row.day.strftime("%Y-%m-%d"), value=row.count)
            for row in result.all()
        ]

    async def query_activity(self, days: int = 30) -> list[TimeSeriesPoint]:
        stmt = (
            select(
                func.date_trunc("day", QueryLog.created_at).label("day"),
                func.count(QueryLog.id).label("count"),
            )
            .where(QueryLog.created_at >= func.now() - text(f"interval '{days} days'"))
            .group_by("day")
            .order_by("day")
        )
        result = await self.db.execute(stmt)
        return [
            TimeSeriesPoint(date=row.day.strftime("%Y-%m-%d"), value=row.count)
            for row in result.all()
        ]
