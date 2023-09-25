from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_STR: str = "/api/v1"
    API_TITLE: str = "Side Project Share API Docs"
    API_DESC: str = "Side Project 分享平台的 API 文件"
    SQLALCHEMY_DATABASE_URI: Optional[str] = "sqlite:///database.db"


settings = Settings()
