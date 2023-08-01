from typing import AsyncGenerator

import pytest
from fastapi import Depends, FastAPI, Response
from fastapi.responses import JSONResponse
from httpx import AsyncClient

from zimran.fastapi import create_app
from zimran.fastapi.dependencies import get_user_id


@pytest.fixture
def app() -> FastAPI:
    app_ = create_app()

    async def endpoint(user_id: int = Depends(get_user_id)) -> Response:
        return JSONResponse({'user_id': user_id})

    app_.add_api_route('/endpoint', endpoint)
    app_.add_api_route('/user-id/', endpoint)
    return app_


@pytest.fixture
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as async_client:
        yield async_client
