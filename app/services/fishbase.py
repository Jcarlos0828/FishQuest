import asyncio
import duckdb
from app.services.hf_client import table_url, ServerType


def _query_species_count(url: str) -> int:
    con = duckdb.connect()
    result = con.execute(f"SELECT COUNT(*) FROM read_parquet('{url}')").fetchone()
    con.close()
    return result[0]


async def get_health(server: ServerType = "fishbase", version: str = "v25.04") -> dict:
    url = await table_url("species", server=server, version=version)
    count = await asyncio.to_thread(_query_species_count, url)
    return {
        "status": "available",
        "server": server,
        "version": version,
        "source": url,
        "species_count": count,
    }
