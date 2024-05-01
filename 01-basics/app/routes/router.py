from fastapi.routing import APIRouter

from app.routes import query

api_router = APIRouter(prefix="/api")
api_router.include_router(query.router, prefix="/query", tags=["Query Parameters"])
