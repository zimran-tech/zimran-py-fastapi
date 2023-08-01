from fastapi import status
from httpx import AsyncClient


async def test_unauthorized(client: AsyncClient) -> None:
    response = await client.get('/user-id/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test(client: AsyncClient) -> None:
    response = await client.get('/user-id/', headers={'x-zmrn-user-id': '1'})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'user_id': 1}
