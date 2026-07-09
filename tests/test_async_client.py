import pytest



@pytest.mark.asyncio
async def test_async_context():


    from moex_iss import AsyncISSClient


    async with AsyncISSClient() as client:

        assert client is not None