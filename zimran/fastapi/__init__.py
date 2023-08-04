from typing import Any

from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from zimran.config import Environment

_PRODUCTION_APPLICATION_KWARGS = {
    'docs_url': None,
    'redoc_url': None,
    'openapi_url': None,
}


async def _health_handler() -> Response:
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def _get_application_kwargs(environment: Environment) -> dict[str, Any]:
    if environment in {Environment.DEVELOPMENT, Environment.STAGING}:
        return {}

    return _PRODUCTION_APPLICATION_KWARGS


def create_app(environment: Environment) -> FastAPI:
    app = FastAPI(**_get_application_kwargs(environment))
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    app.add_api_route('/health/', _health_handler)

    @app.on_event('startup')
    async def check_trailing_slash() -> None:
        route: APIRoute

        for route in app.routes:  # type: ignore[assignment]
            assert route.path.endswith('/'), "Route path must end with '/'"

    return app
