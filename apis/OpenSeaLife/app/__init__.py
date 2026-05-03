import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from scalar_fastapi import AgentScalarConfig, get_scalar_api_reference

from app.error_handlers import register as register_error_handlers
from app.routes.catalog import router as catalog_router
from app.routes.health import router as health_router
from app.routes.ropensci_fishbase import router as ropensci_fishbase_router

_logger = logging.getLogger("uvicorn.error")

SCALAR_CUSTOM_CSS = """
/* Visual divider between the default-style query params and the optional
   filters in ropensci-fishbase endpoints. Relies on the param order
   convention documented in docs/backlog.md:
     1. server   2. version   3. limit   4. offset   5. include_total
     6+. nullable filters
   Brittle: targets the 6th .parameter-item by position. Scalar exposes no
   data-name attribute to scope by parameter name. If a future endpoint in
   the API deviates from the 5-default convention, the divider lands in the
   wrong place. */
.parameter-item:nth-child(5) {
  padding-bottom: 0.75rem;
  box-shadow: inset 0 -14px 14px -10px rgba(0, 0, 0, 0.7);
}
.parameter-item:nth-child(6) {
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  box-shadow: inset 0 14px 14px -10px rgba(0, 0, 0, 0.7);
}
"""

OPENAPI_TAGS = [
    {
        "name": "health",
        "description": "Connectivity check against the HuggingFace Parquet source.",
    },
    {
        "name": "catalog",
        "description": "Discovery of tables and their column schemas.",
    },
    {
        "name": "ropensci-fishbase",
        "description": (
            "Endpoints inherited from the deprecated fishbaseapi.readme.io contract. "
            "Surfaced because they were historically requested as the canonical query "
            "shape for FishBase and SeaLifeBase. Backed by the same HuggingFace "
            "Parquet datasets exposed by /tables."
        ),
    },
]


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
        openapi_tags=OPENAPI_TAGS,
    )

    @app.get("/scalar", include_in_schema=False)
    async def scalar_ui() -> HTMLResponse:
        return get_scalar_api_reference(
            openapi_url=app.openapi_url,
            title=app.title,
            agent=AgentScalarConfig(disabled=True),
            custom_css=SCALAR_CUSTOM_CSS,
        )

    register_error_handlers(app)

    app.include_router(health_router)
    app.include_router(catalog_router)
    app.include_router(ropensci_fishbase_router)
    return app
