from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.schemas.chart import ChartDataPoint, TimeSeriesPoint
from app.services.chart_builder import ChartBuilder

router = APIRouter(prefix="/charts", tags=["charts"])


@router.get("/source-distribution", response_model=list[ChartDataPoint])
async def source_distribution(
    db: AsyncSession = Depends(get_db),
) -> list[ChartDataPoint]:
    builder = ChartBuilder(db)
    data = await builder.source_distribution()
    return [ChartDataPoint(label=d.label, value=d.value) for d in data]


@router.get("/ingestion-timeline", response_model=list[TimeSeriesPoint])
async def ingestion_timeline(
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
) -> list[TimeSeriesPoint]:
    builder = ChartBuilder(db)
    data = await builder.ingestion_timeline(days=days)
    return [TimeSeriesPoint(date=d.date, value=d.value) for d in data]


@router.get("/query-activity", response_model=list[TimeSeriesPoint])
async def query_activity(
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
) -> list[TimeSeriesPoint]:
    builder = ChartBuilder(db)
    data = await builder.query_activity(days=days)
    return [TimeSeriesPoint(date=d.date, value=d.value) for d in data]
