import asyncio
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from zimran.config import Environment

_DEVELOPMENT_APPLICATION_DOCS_KWARGS = {
    'docs_url': '/docs/',
    'redoc_url': '/redoc/',
    'swagger_ui_oauth2_redirect_url': '/docs/oauth2-redirect/',
    'openapi_url': '/schema/',
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


def create_app(environment: Environment, **kwargs) -> FastAPI:  # type: ignore
    kwargs.setdefault('title', 'Zimran App')
    kwargs.update(_get_application_docs_kwargs(environment))

    async def _check_trailing_slash(routes):
        for route in routes:
            assert route.path.endswith('/'), f"Route '{route.path}' must end with '/'"

    async def _check_deprecated_hooks(app: FastAPI):
        if any([
            app.router.on_startup, app.router.on_shutdown,
            kwargs.get('on_startup'), kwargs.get('on_shutdown'),
        ]):
            raise Exception('Cannot use on_startup or on_shutdown with lifespan context manager')

    if lifespan_ := kwargs.pop('lifespan', None):
        @asynccontextmanager
        async def _lifespan(app: FastAPI) -> None:
            async with lifespan_(app):
                await asyncio.gather(
                    _check_trailing_slash(app.routes), _check_deprecated_hooks(app),
                )

                yield
    else:
        @asynccontextmanager
        async def _lifespan(app: FastAPI) -> None:
            await asyncio.gather(_check_trailing_slash(app.routes), _check_deprecated_hooks(app))

            yield

    kwargs['lifespan'] = _lifespan

    app = FastAPI(**kwargs)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    app.add_api_route('/health/', _health_handler)

    return app
