from os.path import join

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, ORJSONResponse
from fastapi.staticfiles import StaticFiles

from app.app_paths import app_paths
from app.auth.auth_handler import auth_handler
from app.core.env_settings import env_settings
from app.models.user_model import User, UserResponse
from app.routes.lifetime import lifespan
from app.routes.router import api_router
from app.routes.user.user_view import login


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """

    app = FastAPI(
        title=env_settings.APP_NAME,
        description=env_settings.APP_DESC,
        version=env_settings.APP_VERSION,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
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

    # * GET
    @app.get("/users/me")
    async def get_logged_in_user(
        user: User = Depends(auth_handler.get_current_user),
    ) -> UserResponse:
        return user  # type: ignore

    # Add Icon
    @app.get("/favicon.ico", include_in_schema=False)
    async def _() -> FileResponse:
        return FileResponse(join(app_paths.static, "favicon.ico"))

    # Main router for the API.
    app.include_router(router=api_router)

    # from app.routes.user.user_view import login

    # token router for swagger secure APIS
    @app.post("/api/token", include_in_schema=False)
    async def _(result=Depends(login)):
        return result

    # mount static posts
    app.mount("/static", StaticFiles(directory=app_paths.static), name="static")

    return app
