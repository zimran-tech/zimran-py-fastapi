import asyncio
from collections.abc import AsyncIterator, Awaitable, Callable, Iterable, Iterator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from user_agents import parse
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


async def add_user_agent_to_logs(
    request: Request, call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    ua_string = request.headers.get('user-agent', '-')
    user_agent = parse(ua_string)

    platform = 'web'
    if user_agent.is_mobile:
        if 'android' in user_agent.os.family.lower():
            platform = 'android'
        elif 'ios' in user_agent.os.family.lower() or 'iphone' in user_agent.os.family.lower():
            platform = 'ios'

    with logger.contextualize(platform=platform):
        response: Response = await call_next(request)
        logger.info('{} {} {} {}', request.method, request.url.path, response.status_code, platform)
        return response


def _iter_route_paths(routes: Iterable[Any]) -> Iterator[str]:
    for route in routes:
        path = getattr(route, 'path', None)
        if isinstance(path, str):
            yield path
        elif (included_router := getattr(route, 'original_router', None)) is not None:
            # since fastapi 0.139 `include_router` registers a pathless proxy route
            # wrapping the original router instead of flattening its routes
            yield from _iter_route_paths(included_router.routes)


def _get_application_docs_kwargs(environment: Environment) -> dict[str, Any]:
    if environment in {Environment.DEVELOPMENT, Environment.STAGING}:
        return _DEVELOPMENT_APPLICATION_DOCS_KWARGS

    return _PRODUCTION_APPLICATION_DOCS_KWARGS


def create_app(environment: Environment, **kwargs: Any) -> FastAPI:
    kwargs.setdefault('title', 'Zimran App')
    kwargs.update(_get_application_docs_kwargs(environment))

    async def _check_trailing_slash(routes: Iterable[Any]) -> None:
        for path in _iter_route_paths(routes):
            assert path.endswith('/'), f"Route '{path}' must end with '/'"

    async def _check_deprecated_hooks(app: FastAPI) -> None:
        if any([
            app.router.on_startup, app.router.on_shutdown,
            kwargs.get('on_startup'), kwargs.get('on_shutdown'),
        ]):
            raise Exception('Cannot use on_startup or on_shutdown with lifespan context manager')

    if lifespan_ := kwargs.pop('lifespan', None):
        @asynccontextmanager
        async def _lifespan(app: FastAPI) -> AsyncIterator[None]:
            async with lifespan_(app):
                await asyncio.gather(
                    _check_trailing_slash(app.routes), _check_deprecated_hooks(app),
                )

                yield
    else:
        @asynccontextmanager
        async def _lifespan(app: FastAPI) -> AsyncIterator[None]:
            await asyncio.gather(_check_trailing_slash(app.routes), _check_deprecated_hooks(app))

            yield

    kwargs['lifespan'] = _lifespan

    app = FastAPI(**kwargs)

    app.middleware('http')(add_user_agent_to_logs)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    app.add_api_route('/health/', _health_handler)

    return app
