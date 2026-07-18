import asyncio

from moex_iss.clients.async_client import AsyncISSClient

URLS = [
    "https://iss.moex.com/iss/engines.json",
    "https://iss.moex.com/iss/engines/stock/markets.json",
]


async def main():

    async with AsyncISSClient() as client:
        tasks = [client.get_json(url) for url in URLS]

        result = await asyncio.gather(*tasks)

        for item in result:
            print(item.keys())


asyncio.run(main())
