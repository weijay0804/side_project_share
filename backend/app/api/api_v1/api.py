from fastapi import APIRouter

from app.api.api_v1.endpoints import user, project, auth, topic

api_router = APIRouter()
api_router.include_router(user.router, prefix="/users", tags=["使用者資源 endpoint"])
api_router.include_router(project.router, prefix="/projects", tags=["專案計畫資源 endpoint"])
api_router.include_router(auth.router, prefix="/auth", tags=["使用者認證 endpoint"])
api_router.include_router(topic.router, prefix="/topic", tags=["專案種類 endpoint"])
