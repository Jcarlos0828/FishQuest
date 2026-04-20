import asyncio
from typing import Any

import duckdb

from app.services.hf_client import ServerType, list_table_urls


def _describe_table(url: str) -> list[dict[str, str]]:
    try:
        con = duckdb.connect()
        rows = con.execute(f"DESCRIBE SELECT * FROM read_parquet('{url}')").fetchall()
        con.close()
        return [{"name": row[0], "type": row[1]} for row in rows]
    except Exception:
        return []


async def get_tables(
    server: ServerType = "fishbase", version: str = "v25.04"
) -> dict[str, Any]:
    table_urls = await list_table_urls(server=server, version=version)

    async def describe(name: str, url: str) -> dict[str, Any]:
        columns = await asyncio.to_thread(_describe_table, url)
        return {"name": name, "columns": columns}

    tables = await asyncio.gather(
        *[describe(name, url) for name, url in sorted(table_urls.items())]
    )

    return {
        "server": server,
        "version": version,
        "total": len(tables),
        "tables": list(tables),
    }
