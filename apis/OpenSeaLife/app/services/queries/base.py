from typing import Any

import duckdb
from common.base.service import BaseService

from app.config import settings
from app.exceptions import (
    DataSourceError,
    InvalidVersionError,
    TableNotFoundError,
)
from app.services.hf_client import (
    ServerType,
    available_versions,
    list_table_urls,
)


class QueryService(BaseService):
    """Generic paginated query against a Parquet table on HuggingFace.

    Subclasses declare `table_name` and `allowed_filters` (param → column).
    """

    table_name: str = ""
    allowed_filters: dict[str, str] = {}

    async def fetch_page(
        self,
        server: ServerType,
        version: str | None,
        filters: dict[str, Any],
        limit: int,
        offset: int,
        include_total: bool,
    ) -> dict[str, Any]:
        ver = version or settings.default_version

        versions = await available_versions(server)
        if ver not in versions:
            raise InvalidVersionError(
                version=ver, server=server, available=sorted(versions)
            )

        try:
            urls = await list_table_urls(server=server, version=ver)
        except Exception as e:
            raise DataSourceError(f"Cannot list tables on HuggingFace: {e}") from e

        if self.table_name not in urls:
            raise TableNotFoundError(table=self.table_name, server=server, version=ver)

        url = urls[self.table_name]

        active = {
            self.allowed_filters[k]: v
            for k, v in filters.items()
            if v is not None and k in self.allowed_filters
        }

        try:
            page = await self.run_sync(
                _execute_query, url, active, limit, offset, include_total
            )
        except Exception as e:
            raise DataSourceError(f"Query failed against Parquet: {e}") from e

        return {
            "server": server,
            "version": ver,
            "limit": limit,
            "offset": offset,
            "total": page["total"],
            "items": page["items"],
        }


def _execute_query(
    url: str,
    filters: dict[str, Any],
    limit: int,
    offset: int,
    include_total: bool,
) -> dict[str, Any]:
    where = ""
    params: list[Any] = []
    if filters:
        clauses = [f'"{col}" = ?' for col in filters]
        where = " WHERE " + " AND ".join(clauses)
        params = list(filters.values())

    con = duckdb.connect()
    try:
        sql = f"SELECT * FROM read_parquet('{url}'){where} " f"LIMIT ? OFFSET ?"
        cursor = con.execute(sql, [*params, limit, offset])
        columns = [d[0] for d in cursor.description] if cursor.description else []
        rows = cursor.fetchall()
        items = [dict(zip(columns, row, strict=True)) for row in rows]

        total: int | None = None
        if include_total:
            count_sql = f"SELECT COUNT(*) FROM read_parquet('{url}'){where}"
            result = con.execute(count_sql, params).fetchone()
            total = int(result[0]) if result else 0
    finally:
        con.close()

    return {"items": items, "total": total}
