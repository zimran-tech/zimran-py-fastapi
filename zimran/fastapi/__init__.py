from typing import Any

from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from starlette.types import Lifespan

from zimran.config import Environment

_DEVELOPMENT_APPLICATION_DOCS_KWARGS = {
    'docs_url': '/docs/',
    'redoc_url': '/redoc/',
    'swagger_ui_oauth2_redirect_url': '/docs/oauth2-redirect/',
    'openapi_url': '/openapi.json/',
}

_PRODUCTION_APPLICATION_DOCS_KWARGS = {
    'docs_url': None,
    'redoc_url': None,
    'swagger_ui_oauth2_redirect_url': None,
    'openapi_url': None,
}


async def _health_handler() -> Response:
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def _get_application_docs_kwargs(environment: Environment) -> dict[str, Any]:
    if environment in {Environment.DEVELOPMENT, Environment.STAGING}:
        return _DEVELOPMENT_APPLICATION_DOCS_KWARGS

    return _PRODUCTION_APPLICATION_DOCS_KWARGS


def create_app(environment: Environment, **kwargs) -> FastAPI:
    kwargs.setdefault('title', 'Zimran App')

    kwargs.update(_get_application_docs_kwargs(environment))

    app = FastAPI(**kwargs)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    app.add_api_route('/health/', _health_handler)

    for route in app.routes:  # type: ignore[assignment]
        assert route.path.endswith('/'), f"Route '{route.path}' must end with '/'"

    return app
