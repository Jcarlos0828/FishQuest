from typing import Annotated, Literal

from fastapi import APIRouter, Query

from app.config import settings
from app.error_handlers import PROBLEM_RESPONSES
from app.schemas.queries.comnames import ComnamesPage, ComnamesRow
from app.services.queries.comnames import ComnamesService

router = APIRouter()
_service = ComnamesService()

ServerParam = Annotated[Literal["fishbase", "sealifebase"], Query()]


@router.get("/comnames", response_model=ComnamesPage, responses=PROBLEM_RESPONSES)
async def list_comnames(
    server: ServerParam = "fishbase",
    version: Annotated[str, Query()] = settings.default_version,
    limit: Annotated[int, Query(ge=1, le=500)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
    include_total: Annotated[
        bool,
        Query(
            description=(
                "If true, the response includes `total` — the total number of "
                "rows matching the current filters across all pages."
            ),
        ),
    ] = False,
    spec_code: Annotated[int | None, Query()] = None,
    language: Annotated[str | None, Query()] = None,
    c_code: Annotated[str | None, Query()] = None,
    name_type: Annotated[str | None, Query()] = None,
    preferred_name: Annotated[bool | None, Query()] = None,
) -> ComnamesPage:
    data = await _service.fetch_page(
        server=server,
        version=version,
        filters={
            "spec_code": spec_code,
            "language": language,
            "c_code": c_code,
            "name_type": name_type,
            "preferred_name": (
                int(preferred_name) if preferred_name is not None else None
            ),
        },
        limit=limit,
        offset=offset,
        include_total=include_total,
    )
    return ComnamesPage(
        server=data["server"],
        version=data["version"],
        limit=data["limit"],
        offset=data["offset"],
        total=data["total"],
        items=[ComnamesRow.model_validate(row) for row in data["items"]],
    )
