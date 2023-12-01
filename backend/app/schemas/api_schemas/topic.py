from typing import Optional

from pydantic import BaseModel


class Topic(BaseModel):
    id: int
    name: str


class TopicCreate(BaseModel):
    name: str


class TopicUpdate(BaseModel):
    name: Optional[str] = None
