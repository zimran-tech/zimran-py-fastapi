from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware


async def _health_handler() -> Response:
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def create_app() -> FastAPI:
    app = FastAPI(docs_url=None, redoc_url=None)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    app.add_api_route('/health/', _health_handler)
    return app
