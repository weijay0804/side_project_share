from typing import Optional, List
from pydantic import BaseModel


class User(BaseModel):
    """使用者資源詳細資料"""

    id: int
    username: str
    email: str
    avatar_url: Optional[str] = None
    city: Optional[str] = None
    age: Optional[str] = None
    gender: Optional[str] = None
    is_email_public: bool
    github: Optional[str] = None
    is_github_public: bool
    discord: Optional[str] = None
    is_discord_public: bool
    skill: Optional[List[str]] = None


class UserCreate(BaseModel):
    """建立使用者資源"""

    username: str
    email: str
    password: str


class UserUpdate(BaseModel):
    """更新使用者資源"""

    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    avatar_url: Optional[str] = None
    city: Optional[str] = None
    age: Optional[str] = None
    gender: Optional[str] = None
    is_email_public: Optional[bool] = None
    github: Optional[str] = None
    is_github_public: Optional[bool] = None
    discord: Optional[str] = None
    is_discrod_public: Optional[bool] = None
    skill: Optional[List[str]] = None


class UserSimple(BaseModel):
    """使用者資源資料（簡易）"""

    id: int
    username: str
    avatar_url: Optional[str] = None
