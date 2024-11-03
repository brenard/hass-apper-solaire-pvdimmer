"""Helpers for component."""

import asyncio
import logging
from typing import Any

from aiohttp import ClientSession

_LOGGER = logging.getLogger(__name__)


async def async_request(
    session: ClientSession,
    url: str,
    method: str = "get",
    timeout: int = 5,
    json_decode: bool = True,
    **kwargs: Any,
) -> Any:
    """Request url with method."""
    session = session or ClientSession()
    async with asyncio.timeout(timeout):
        _LOGGER.debug("Request: %s (%s) - %s", url, method, kwargs.get("params", "No parameter"))
        response = await session.request(method, url, **kwargs)
        result = (
            await response.json(content_type=None)
            if json_decode
            else (await response.read()).decode("utf8")
        )
        _LOGGER.debug("Result (%s): %s", response.status, result)
        response.raise_for_status()
        return result
