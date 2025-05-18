from contextlib import asynccontextmanager

from fastapi.responses import ORJSONResponse
from src.api.routers import main_router
from src.core.config import project_settings, redis_settings
from src.db.redis_cache import RedisCacheManager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление ресурсами FastAPI."""

    redis_cache_manager = RedisCacheManager(redis_settings)
    try:
        await redis_cache_manager.setup()
        yield

    finally:
        await redis_cache_manager.tear_down()

app = FastAPI(
    title=project_settings.name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    summary=project_settings.summary,
    version=project_settings.version,
    terms_of_service=project_settings.terms_of_service,
    openapi_tags=project_settings.tags,
    lifespan=lifespan,
)

app.include_router(main_router)
