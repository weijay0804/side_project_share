from typing import Optional
from pydantic import BaseModel

from app.schemas.db_schemas.user import UserDBCreaet, UserInDB, UserDBUpdate


class User(UserInDB):
    """使用者資源資料"""

    pass


class UserCreate(UserDBCreaet):
    """建立使用者資源"""

    pass


class UserUpdate(UserDBUpdate):
    """更新使用者資源"""

    pass


class UserSimple(BaseModel):
    """使用者資源資料（簡易）"""

    id: int
    username: str
    avatar_url: Optional[str] = None
