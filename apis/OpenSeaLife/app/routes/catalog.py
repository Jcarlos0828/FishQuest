from typing import Annotated, Literal

from common.catalog.schemas import TablesResponse
from fastapi import APIRouter, HTTPException, Query

from app.config import settings
from app.services.catalog import CatalogService

router = APIRouter(tags=["catalog"])

ServerParam = Annotated[Literal["fishbase", "sealifebase"], Query()]
VersionParam = Annotated[str, Query()]

_service = CatalogService()


@router.get("/tables", response_model=TablesResponse)
async def tables(
    server: ServerParam = "fishbase",
    version: VersionParam = settings.default_version,
) -> TablesResponse:
    try:
        data = await _service.get_tables(server=server, version=version)
        return TablesResponse(**data)
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
