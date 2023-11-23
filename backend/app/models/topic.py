from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from .intermediary import project_topic_table


class Topic(Base):
    __tablename__ = "topic"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True, unique=True, nullable=False)
    create_at = Column(DateTime, default=datetime.utcnow)

    # 與 project table 建立多對多關係
    projects = relationship(
        "Project", secondary=project_topic_table, back_populates="topics", lazy="dynamic"
    )
