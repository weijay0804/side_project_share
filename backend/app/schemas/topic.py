from typing import Optional

from pydantic import BaseModel


class TopicInDB(BaseModel):
    topic_id: Optional[int] = None
    name: Optional[str] = None

    class ConfigDict:
        from_attributes = True
        extra = "ignore"
