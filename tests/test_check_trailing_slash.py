import pytest
from fastapi import APIRouter, FastAPI, Response
from fastapi.testclient import TestClient
from zimran.config import Environment

from zimran.fastapi import create_app


async def _handler() -> Response:
    return Response()


@pytest.mark.xfail(raises=AssertionError, strict=True)
async def test(app: FastAPI) -> None:
    with TestClient(app):
        pass


async def test_included_router() -> None:
    nested_router = APIRouter()
    nested_router.add_api_route('/items/', _handler)

    router = APIRouter()
    router.add_api_route('/users/', _handler)
    router.include_router(nested_router, prefix='/nested')

    app_ = create_app(Environment.DEVELOPMENT)
    app_.include_router(router, prefix='/v1')

    with TestClient(app_):
        pass


@pytest.mark.xfail(raises=AssertionError, strict=True)
async def test_included_router_without_trailing_slash() -> None:
    router = APIRouter()
    router.add_api_route('/users', _handler)

    app_ = create_app(Environment.DEVELOPMENT)
    app_.include_router(router, prefix='/v1')

    with TestClient(app_):
        pass
