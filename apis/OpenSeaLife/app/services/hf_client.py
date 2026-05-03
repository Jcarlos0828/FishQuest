import asyncio
import json
import ssl
import urllib.request
from typing import Any, Literal

from app.config import settings

_ssl_ctx = ssl.create_default_context()
_ssl_ctx.check_hostname = False
_ssl_ctx.verify_mode = ssl.CERT_NONE

ServerType = Literal["fishbase", "sealifebase"]


def _fetch_json(url: str) -> Any:
    with urllib.request.urlopen(url, timeout=10, context=_ssl_ctx) as r:
        return json.loads(r.read())


async def fetch_json(url: str) -> Any:
    return await asyncio.to_thread(_fetch_json, url)


async def available_versions(server: ServerType = "fishbase") -> set[str]:
    sv = "fb" if server == "fishbase" else "slb"
    url = (
        f"{settings.hf_base}/api/{settings.hf_repo}"
        f"/tree/{settings.hf_branch}/data/{sv}"
    )
    items: list[dict[str, Any]] = await fetch_json(url)
    return {item["path"].split("/")[-1] for item in items}


async def list_table_urls(
    server: ServerType = "fishbase", version: str | None = None
) -> dict[str, str]:
    sv = "fb" if server == "fishbase" else "slb"
    ver = version or settings.default_version
    path = f"data/{sv}/{ver}/parquet"
    url = f"{settings.hf_base}/api/{settings.hf_repo}/tree/{settings.hf_branch}/{path}"
    items: list[dict[str, Any]] = await fetch_json(url)
    return {
        item["path"].split("/")[-1].replace(".parquet", ""): (
            f"{settings.hf_base}/{settings.hf_repo}/resolve/{settings.hf_branch}/{item['path']}"
        )
        for item in items
    }


async def table_url(
    table: str, server: ServerType = "fishbase", version: str | None = None
) -> str:
    urls = await list_table_urls(server, version)
    if table not in urls:
        ver = version or settings.default_version
        raise KeyError(f"Table '{table}' not found for {server} {ver}.")
    return urls[table]
