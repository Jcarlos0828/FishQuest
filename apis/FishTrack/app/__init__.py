import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from scalar_fastapi import AgentScalarConfig, get_scalar_api_reference

_logger = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    _logger.info("Scalar:      http://localhost:8005/scalar")
    _logger.info("ReDoc:       http://localhost:8005/redoc")
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="FishTrack API",
        description="Species checklist by aquarium.",
        version="0.1.0",
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

    return app
