from typing import Literal

from pydantic import BaseModel


class ColumnSchema(BaseModel):
    name: str
    type: str


class TableInfo(BaseModel):
    name: str
    columns: list[ColumnSchema]


class TablesResponse(BaseModel):
    server: Literal["fishbase", "sealifebase"]
    version: str
    total: int
    tables: list[TableInfo]


class HealthResponse(BaseModel):
    status: Literal["available", "unavailable"]
    server: Literal["fishbase", "sealifebase"]
    version: str
    source: str | None = None
    species_count: int | None = None
    error: str | None = None
