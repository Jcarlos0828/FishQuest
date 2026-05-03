import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from scalar_fastapi import AgentScalarConfig, get_scalar_api_reference

from app.routes.catalog import router as catalog_router
from app.routes.health import router as health_router

_logger = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    _logger.info("Scalar:      http://localhost:8006/scalar")
    _logger.info("ReDoc:       http://localhost:8006/redoc")
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="OpenSeaLife API",
        description=(
            "Acceso centralizado a FishBase y SeaLifeBase "
            "vía HuggingFace Parquet/DuckDB."
        ),
        version="1.0.0",
        lifespan=_lifespan,
        docs_url=None,
    )

    @app.get("/scalar", include_in_schema=False)
    async def scalar_ui() -> HTMLResponse:
        return get_scalar_api_reference(
            openapi_url=app.openapi_url,
            title=app.title,
            agent=AgentScalarConfig(disabled=True),
        )

    app.include_router(health_router)
    app.include_router(catalog_router)
    return app
