import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

_logger = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    _logger.info("Swagger UI:  http://localhost:8005/docs")
    _logger.info("ReDoc:       http://localhost:8005/redoc")
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="FishTrack API",
        description="Species checklist by aquarium.",
        version="0.1.0",
        lifespan=_lifespan,
    )
    return app
