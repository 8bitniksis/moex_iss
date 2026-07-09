from typing import Any, cast

import httpx

from .config import ISSConfig


class AsyncISSClient:
    def __init__(
        self,
        config: ISSConfig | None = None,
    ) -> None:

        self.config = config or ISSConfig()

        self.client = httpx.AsyncClient(
            timeout=self.config.timeout,
            headers={"User-Agent": self.config.user_agent},
        )

    async def close(self) -> None:

        await self.client.aclose()

    async def get_json(
        self,
        url: str,
    ) -> dict[str, Any]:

        response = await self.client.get(url)

        response.raise_for_status()

        return cast(
            dict[str, Any],
            response.json(),
        )

    async def __aenter__(self) -> "AsyncISSClient":

        return self

    async def __aexit__(
        self,
        exc_type: Any,
        exc_value: Any,
        traceback: Any,
    ) -> None:

        await self.close()
