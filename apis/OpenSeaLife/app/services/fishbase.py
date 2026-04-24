from typing import Any

from common.base.service import BaseService
from common.datasource_health.queries import _query_species_count

from app.config import settings
from app.services.hf_client import ServerType, table_url


class FishbaseService(BaseService):
    async def get_health(
        self, server: ServerType = "fishbase", version: str | None = None
    ) -> dict[str, Any]:
        ver = version or settings.default_version
        url = await table_url("species", server=server, version=ver)
        count = await self.run_sync(_query_species_count, url)
        return {
            "status": "available",
            "server": server,
            "version": ver,
            "source": url,
            "species_count": count,
        }
