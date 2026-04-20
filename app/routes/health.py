from fastapi import APIRouter, HTTPException
from typing import Annotated, Literal
from fastapi import Query
from app.schemas import HealthResponse
from app.services.fishbase import get_health

router = APIRouter(tags=["health"])

ServerParam = Annotated[Literal["fishbase", "sealifebase"], Query()]
VersionParam = Annotated[str, Query()]


@router.get("/health", response_model=HealthResponse)
async def health(
    server: ServerParam = "fishbase",
    version: VersionParam = "v25.04",
) -> HealthResponse:
    try:
        data = await get_health(server=server, version=version)
        return HealthResponse(**data)
    except Exception as e:
        return HealthResponse(
            status="unavailable",
            server=server,
            version=version,
            error=str(e),
        )
