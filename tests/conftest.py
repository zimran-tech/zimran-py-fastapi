from typing import AsyncGenerator

import pytest
from httpx import AsyncClient

from zimran.fastapi import create_app


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    app = create_app()

    async with AsyncClient(app=app, base_url='http://test') as async_client:
        yield async_client
