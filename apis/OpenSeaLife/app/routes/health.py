from typing import Annotated, Literal

from common.datasource_health.schemas import HealthResponse
from fastapi import APIRouter, Query

from app.config import settings
from app.services.fishbase import FishbaseService

router = APIRouter(tags=["health"])

ServerParam = Annotated[Literal["fishbase", "sealifebase"], Query()]
VersionParam = Annotated[str, Query()]

_service = FishbaseService()


@router.get("/datasource/health", response_model=HealthResponse)
async def health(
    server: ServerParam = "fishbase",
    version: VersionParam = settings.default_version,
) -> HealthResponse:
    try:
        data = await _service.get_health(server=server, version=version)
        return HealthResponse(**data)
    except Exception as e:
        return HealthResponse(
            status="unavailable",
            server=server,
            version=version,
            error=str(e),
        )
