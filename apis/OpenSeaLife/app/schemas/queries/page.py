from typing import Generic, Literal, TypeVar

from common.base.models import BaseApiModel

T = TypeVar("T")


class PageEnvelope(BaseApiModel, Generic[T]):
    server: Literal["fishbase", "sealifebase"]
    version: str
    limit: int
    offset: int
    total: int | None = None
    items: list[T]
