from fastapi.routing import APIRouter

from app.routes import user

# from app.routes.user.user_view import token_router

api_router = APIRouter(prefix="/api")

# api_router.include_router(token_router, include_in_schema=False)

api_router.include_router(user.router, prefix="/users", tags=["User"])
