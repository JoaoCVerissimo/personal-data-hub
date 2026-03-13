from fastapi import APIRouter

from app.api.charts import router as charts_router
from app.api.documents import router as documents_router
from app.api.jobs import router as jobs_router
from app.api.query import router as query_router
from app.api.sources import router as sources_router

api_router = APIRouter()
api_router.include_router(sources_router)
api_router.include_router(jobs_router)
api_router.include_router(query_router)
api_router.include_router(documents_router)
api_router.include_router(charts_router)
