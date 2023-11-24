from typing import Optional

from pydantic import BaseModel


class TopicInDB(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None

    class ConfigDict:
        from_attributes = True
        extra = "ignore"


class TopicDBCreate(TopicInDB):
    pass


class TopicDBUpdate(TopicInDB):
    pass
