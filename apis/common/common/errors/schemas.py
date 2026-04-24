from common.base.models import BaseApiModel


class ProblemDetail(BaseApiModel):
    type: str
    title: str
    status: int
    detail: str | None = None
    instance: str | None = None
