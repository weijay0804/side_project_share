from typing import Optional, List
from pydantic import BaseModel


class Project(BaseModel):
    """專案資源詳細資料"""

    id: int
    host_username: str
    host_user_avatar_url: Optional[str] = None
    title: str
    max_member_number: int
    status: str
    intor: Optional[str] = None
    desc: Optional[str] = None
    image_url: Optional[str] = None
    topic: Optional[list] = None
    member: Optional[list] = None


class ProjectSimple(BaseModel):
    """專案資源資料（簡易）"""

    id: int
    host_username: str
    host_user_avatar_url: Optional[str] = None
    title: str
    status: str
    topic: Optional[list] = None


class ProjectMe(BaseModel):
    """屬於使用者的專案資源資料"""

    id: int
    title: str
    status: str
    topic: Optional[list] = None


class ProjectUpdate(BaseModel):
    """更新專案資源"""

    title: Optional[str] = None
    max_member_number: Optional[int] = None
    status: Optional[str] = None
    intor: Optional[str] = None
    desc: Optional[str] = None
    image_url: Optional[str] = None


class ProjectCreate(BaseModel):
    """建立專案資源"""

    title: str
    max_member_number: int
    status: str
    intro: Optional[str] = None
    desc: Optional[str] = None
    image_url: Optional[str] = None
    topic_id_list: Optional[List[int]] = None
