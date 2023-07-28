from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute


async def _health_handler() -> Response:
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def create_app() -> FastAPI:
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
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
