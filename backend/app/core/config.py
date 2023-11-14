from typing import Optional
import os

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    API_STR: str = "/api/v1"
    API_TITLE: str = "Side Project Share API Docs"
    API_DESC: str = "Side Project 分享平台的 API 文件"
    SQLALCHEMY_DATABASE_URI: Optional[str] = os.getenv("DATABASE_URI", "sqlite:///database.db")
    JWT_SRCRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_TOKEN_EXP_MIN: int = os.getenv("JWT_TOKEN_EXP_MIN", 30)


settings = Settings()
