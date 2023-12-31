from typing import AsyncGenerator

import pytest
from fastapi import Depends, FastAPI, Response
from fastapi.responses import JSONResponse
from httpx import AsyncClient
from zimran.config import Environment

from zimran.fastapi import create_app
from zimran.fastapi.dependencies import get_user_id


@pytest.fixture
def app() -> FastAPI:
    app_ = create_app(Environment.DEVELOPMENT)

    async def handler(user_id: int = Depends(get_user_id)) -> Response:
        return JSONResponse({'user_id': user_id})

    app_.add_api_route('/without-trailing-slash', handler)
    app_.add_api_route('/user-id/', handler)
    return app_


@pytest.fixture
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as async_client:
        yield async_client
