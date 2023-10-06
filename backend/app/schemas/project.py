from typing import Optional, List

from pydantic import BaseModel

from .topic import TopicInDB
from .user import UserSimple


class ProjectBase(BaseModel):
    title: str
    max_member_number: Optional[int] = None


class ProjectInDBBase(ProjectBase):
    id: Optional[int] = None
    current_member_number: int = None
    status: str = None
    intro: str = None


class ProjectInBD(ProjectInDBBase):
    desc: str = None
    image_url: str = None

    class ConfigDict:
        from_attributes = True
        extra = "ignore"


class ProjectSimple(ProjectInDBBase):
    host_username: str
    host_user_avatar_url: str
    topic: List[TopicInDB]


class ProjectCreate(ProjectBase):
    intro: Optional[str] = None
    desc: Optional[str] = None
    image_url: Optional[str] = None
    topic_id_list: Optional[List[int]] = None


class ProjectUserRead(ProjectInDBBase):
    topic: List[TopicInDB]


class Project(ProjectInBD):
    host_username: str
    host_avatar_url: str
    topic: List[TopicInDB]
    member: List[UserSimple]
