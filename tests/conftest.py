from typing import AsyncGenerator

import pytest
from fastapi import FastAPI, Response, status
from httpx import AsyncClient

from zimran.fastapi import create_app


@pytest.fixture
def app() -> FastAPI:
    app_ = create_app()

    async def endpoint() -> Response:
        return Response(status_code=status.HTTP_200_OK)

    app_.add_api_route('/endpoint', endpoint)
    return app_


@pytest.fixture
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as async_client:
        yield async_client
