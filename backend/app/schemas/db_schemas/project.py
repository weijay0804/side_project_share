from typing import Optional
from pydantic import BaseModel


class ProjectInBD(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    max_member_number: Optional[int] = None
    current_member_number: Optional[int] = None
    status: Optional[str] = None
    intro: Optional[str] = None
    desc: Optional[str] = None
    image_url: Optional[str] = None

    class ConfigDict:
        from_attributes = True
        extra = "ignore"


class ProjectDBCreate(BaseModel):
    title: str
    max_member_number: int
    intro: Optional[str] = None
    desc: Optional[str] = None
    image_url: Optional[str] = None


class ProjectDBUpdate(BaseModel):
    title: Optional[str] = None
    max_member_number: Optional[int] = None
    current_member_number: Optional[int] = None
    status: Optional[str] = None
    intro: Optional[str] = None
    desc: Optional[str] = None
    image_url: Optional[str] = None
