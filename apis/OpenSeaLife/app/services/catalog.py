import asyncio
from typing import Any

from common.base.service import BaseService
from common.catalog.queries import _describe_table

from app.config import settings
from app.services.hf_client import ServerType, list_table_urls


class CatalogService(BaseService):
    async def get_tables(
        self, server: ServerType = "fishbase", version: str | None = None
    ) -> dict[str, Any]:
        ver = version or settings.default_version
        table_urls = await list_table_urls(server=server, version=ver)

        async def describe(name: str, url: str) -> dict[str, Any]:
            columns = await self.run_sync(_describe_table, url)
            return {"name": name, "columns": columns}

        tables = await asyncio.gather(
            *[describe(name, url) for name, url in sorted(table_urls.items())]
        )

        return {
            "server": server,
            "version": ver,
            "total": len(tables),
            "tables": list(tables),
        }
