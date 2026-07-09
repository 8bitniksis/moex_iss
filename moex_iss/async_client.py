import httpx

from .config import ISSConfig


class AsyncISSClient:


    def __init__(
        self,
        config=None
    ):

        self.config = (
            config
            or ISSConfig()
        )


        self.client = (
            httpx.AsyncClient(
                timeout=
                    self.config.timeout,
                headers={
                    "User-Agent":
                    self.config.user_agent
                }
            )
        )



    async def close(self):

        await self.client.aclose()



    async def get_json(
        self,
        url
    ):


        response = await (
            self.client.get(url)
        )


        response.raise_for_status()


        return response.json()



    async def __aenter__(
        self
    ):

        return self



    async def __aexit__(
        self,
        *args
    ):

        await self.close()