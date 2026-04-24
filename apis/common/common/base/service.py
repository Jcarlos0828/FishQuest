import asyncio
from collections.abc import Callable
from typing import Any, TypeVar

T = TypeVar("T")


class BaseService:
    @staticmethod
    async def run_sync(func: Callable[..., T], *args: Any) -> T:
        return await asyncio.to_thread(func, *args)
