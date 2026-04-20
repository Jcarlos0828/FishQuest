import asyncio
import json
import ssl
import urllib.request
from typing import Any, Literal

_ssl_ctx = ssl.create_default_context()
_ssl_ctx.check_hostname = False
_ssl_ctx.verify_mode = ssl.CERT_NONE

HF_BASE = "https://huggingface.co"
HF_REPO = "datasets/cboettig/fishbase"
HF_BRANCH = "main"
DEFAULT_VERSION = "v25.04"

ServerType = Literal["fishbase", "sealifebase"]


def _fetch_json(url: str) -> Any:
    with urllib.request.urlopen(url, timeout=10, context=_ssl_ctx) as r:
        return json.loads(r.read())


async def fetch_json(url: str) -> Any:
    return await asyncio.to_thread(_fetch_json, url)


async def available_versions(server: ServerType = "fishbase") -> list[str]:
    sv = "fb" if server == "fishbase" else "slb"
    url = f"{HF_BASE}/api/{HF_REPO}/tree/{HF_BRANCH}/data/{sv}"
    items: list[dict[str, Any]] = await fetch_json(url)
    return [item["path"].split("/")[-1] for item in items]


async def list_table_urls(
    server: ServerType = "fishbase", version: str = DEFAULT_VERSION
) -> dict[str, str]:
    sv = "fb" if server == "fishbase" else "slb"
    path = f"data/{sv}/{version}/parquet"
    url = f"{HF_BASE}/api/{HF_REPO}/tree/{HF_BRANCH}/{path}"
    items: list[dict[str, Any]] = await fetch_json(url)
    return {
        item["path"].split("/")[-1].replace(".parquet", ""): (
            f"{HF_BASE}/{HF_REPO}/resolve/{HF_BRANCH}/{item['path']}"
        )
        for item in items
    }


async def table_url(
    table: str, server: ServerType = "fishbase", version: str = DEFAULT_VERSION
) -> str:
    urls = await list_table_urls(server, version)
    if table not in urls:
        raise KeyError(f"Table '{table}' not found for {server} {version}.")
    return urls[table]
