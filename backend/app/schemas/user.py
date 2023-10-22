from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None


class UserCreaet(UserBase):
    """建立使用者時傳入的資料格式"""

    email: str
    username: str
    password: str


class UserInDBBase(UserBase):
    id: Optional[int] = None


class UserInDB(UserInDBBase):
    avatar_url: Optional[str] = None
    city: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    is_email_public: Optional[bool] = None
    github: Optional[str] = None
    is_github_public: Optional[bool] = None
    discord: Optional[str] = None
    is_discord_public: Optional[bool] = None
    skill: Optional[str] = None

    class ConfigDict:
        from_attributes = True
        extra = "ignore"


class UserSimple(BaseModel):
    user_id: int
    username: str
    avatar_url: str


class User(UserInDB):
    pass


class UserUpdate(UserInDB):
    password: Optional[str] = None
