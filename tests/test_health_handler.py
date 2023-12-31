from fastapi import status
from httpx import AsyncClient


async def test(client: AsyncClient) -> None:
    response = await client.get('/health/')

    assert response.status_code == status.HTTP_204_NO_CONTENT
