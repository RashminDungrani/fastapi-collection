from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from app.routes.lifetime import lifespan
from app.routes.router import api_router


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """

    app = FastAPI(
        title="FastAPI basics",
        description="",
        version="0.0.1",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
        # if platform.system() == "Windows"
        # else None,  # because in macos oracle client is not supported
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Main router for the API.
    app.include_router(router=api_router)

    return app
