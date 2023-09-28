from typing import Optional, List

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str


class UserCreaet(UserBase):
    """建立使用者時傳入的資料格式"""

    password: str


class UserInDBBase(UserBase):
    user_id: Optional[int] = None

    class ConfigDict:
        from_attributes = True
        extra = "ignore"


class UserInDB(UserInDBBase):
    city: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    is_email_public: bool = None
    github: Optional[str] = None
    is_github_public: bool = None
    discord: Optional[str] = None
    is_discord_public: bool = None
    skill: Optional[List[str]] = None


class UserSimple(BaseModel):
    user_id: int
    username: str
    avatar_url: str


class User(UserInDB):
    pass


class UserUpdate(BaseModel):
    city: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    is_email_public: bool = None
    github: Optional[str] = None
    is_github_public: bool = None
    discord: Optional[str] = None
    is_discord_public: bool = None
    skill: Optional[List[str]] = None
