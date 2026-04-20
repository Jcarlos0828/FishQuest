from fastapi import FastAPI

from app.routes.catalog import router as catalog_router
from app.routes.health import router as health_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="FishQuest API",
        description="Acceso a datos de FishBase y SeaLifeBase vía Parquet/DuckDB.",
        version="1.0.0",
    )
    app.include_router(health_router)
    app.include_router(catalog_router)
    return app
