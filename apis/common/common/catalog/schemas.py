from typing import Literal

from common.base.models import BaseApiModel


class ColumnSchema(BaseApiModel):
    name: str
    type: str


class TableInfo(BaseApiModel):
    name: str
    columns: list[ColumnSchema]


class TablesResponse(BaseApiModel):
    server: Literal["fishbase", "sealifebase"]
    version: str
    total: int
    tables: list[TableInfo]
