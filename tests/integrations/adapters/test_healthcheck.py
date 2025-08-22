from httpx import AsyncClient
import pytest

@pytest.mark.asyncio
async def test_healthcheck(client: AsyncClient) -> None:
    response = await client.get("/")

    assert response.status_code == 200