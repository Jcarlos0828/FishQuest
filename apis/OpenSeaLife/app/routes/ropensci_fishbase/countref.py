from typing import Annotated, Literal

from fastapi import APIRouter, Query

from app.config import settings
from app.error_handlers import PROBLEM_RESPONSES
from app.schemas.queries.countref import CountrefPage
from app.services.queries.countref import CountrefService

router = APIRouter()
_service = CountrefService()

ServerParam = Annotated[Literal["fishbase", "sealifebase"], Query()]


@router.get("/countref", response_model=CountrefPage, responses=PROBLEM_RESPONSES)
async def list_countref(
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
    c_code: Annotated[str | None, Query()] = None,
    abb: Annotated[str | None, Query()] = None,
    language: Annotated[str | None, Query()] = None,
    marine_flag: Annotated[bool | None, Query()] = None,
) -> CountrefPage:
    data = await _service.fetch_page(
        server=server,
        version=version,
        filters={
            "c_code": c_code,
            "abb": abb,
            "language": language,
            "marine_flag": (
                (-1 if marine_flag else 0) if marine_flag is not None else None
            ),
        },
        limit=limit,
        offset=offset,
        include_total=include_total,
    )
    return CountrefPage(
        server=data["server"],
        version=data["version"],
        limit=data["limit"],
        offset=data["offset"],
        total=data["total"],
        items=data["items"],
    )
