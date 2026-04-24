from typing import Literal

from common.base.models import BaseApiModel


class HealthResponse(BaseApiModel):
    status: Literal["available", "unavailable"]
    server: Literal["fishbase", "sealifebase"]
    version: str
    source: str | None = None
    species_count: int | None = None
    error: str | None = None
