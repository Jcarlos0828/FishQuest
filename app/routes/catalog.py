from fastapi import APIRouter, HTTPException
from typing import Annotated, Literal
from fastapi import Query
from app.schemas import TablesResponse
from app.services.catalog import get_tables

router = APIRouter(tags=["catalog"])

ServerParam = Annotated[Literal["fishbase", "sealifebase"], Query()]
VersionParam = Annotated[str, Query()]


@router.get("/tables", response_model=TablesResponse)
async def tables(
    server: ServerParam = "fishbase",
    version: VersionParam = "v25.04",
) -> TablesResponse:
    try:
        data = await get_tables(server=server, version=version)
        return TablesResponse(**data)
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
