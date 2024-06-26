from fastapi.routing import APIRouter

from app.routes import body, form, path, query

api_router = APIRouter(prefix="/api")
api_router.include_router(query.router, prefix="/query", tags=["Query"])
api_router.include_router(path.router, prefix="/path", tags=["Path"])
api_router.include_router(body.router, prefix="/body", tags=["Body"])
api_router.include_router(form.router, prefix="/form", tags=["Form"])
