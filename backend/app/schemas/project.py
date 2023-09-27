from typing import Optional, List

from pydantic import BaseModel

from .topic import TopicInDB
from .user import UserSimple


class ProjectBase(BaseModel):
    title: str
    max_number_number: int


class ProjectInDBBase(ProjectBase):
    project_id: Optional[int] = None
    current_member_number: int = None
    status: str = None
    project_intro: str = None


class ProjectInBD(ProjectInDBBase):
    project_desc: str = None
    project_image_url: str = None

    class Config:
        orm_mode = True
        extra = "ignore"


class ProjectSimple(ProjectInDBBase):
    host_username: str
    host_user_avatar_url: str
    topic: List[TopicInDB]


class ProjectCreate(ProjectBase):
    project_intro: Optional[str] = None
    project_desc: Optional[str] = None
    project_image_url: Optional[str] = None
    topic_id_list: Optional[List[int]] = None


class ProjectUserRead(ProjectInDBBase):
    topic: List[TopicInDB]


class Project(ProjectInBD):
    host_username: str
    host_avatar_url: str
    topic: List[TopicInDB]
    member: List[UserSimple]
