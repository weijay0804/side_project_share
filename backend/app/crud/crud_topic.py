from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.topic import Topic
from app.schemas.db_schemas import TopicDBUpdate, TopicDBCreate


class CRUDTopic(CRUDBase[Topic, TopicDBCreate, TopicDBUpdate]):
    def create(self, db: Session, *, obj_in: TopicDBCreate) -> Topic:
        db_obj = Topic(name=obj_in.name)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def get_by_name(self, db: Session, *, name: str) -> Topic:
        topic = db.query(Topic).filter(Topic.name == name).first()

        return topic

    def get_projects(
        self, db: Session, *, topic_id: int, skip: int = 0, limit: int = 100
    ) -> List[Topic]:
        topic = self.get(db, topic_id)

        if topic is None:
            return []

        projects = topic.projects.offset(skip).limit(limit).all()

        return projects


topic = CRUDTopic(Topic)
