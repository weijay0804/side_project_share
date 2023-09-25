from fastapi import FastAPI

from app.core.config import settings
from app.api.api_v1.api import api_router

app = FastAPI(title=settings.API_TITLE, description=settings.API_DESC)

app.include_router(api_router, prefix=settings.API_STR)
