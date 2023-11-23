from datetime import datetime

from sqlalchemy import Column, Integer, String, SmallInteger, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

from .intermediary import project_topic_table


class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True, index=True)
    host_user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    title = Column(String(50), nullable=False)
    max_member_number = Column(SmallInteger, default=10)
    current_member_number = Column(SmallInteger, default=0)
    status = Column(String(20), default="recruit")
    intro = Column(String(50))
    desc = Column(Text)
    image_url = Column(Text)
    create_at = Column(DateTime, default=datetime.utcnow)

    # 建立與 user table 多對一的關係
    user = relationship("User", back_populates="projects")

    # 建立與 topic table 多對多關係
    topics = relationship(
        "Topic", secondary=project_topic_table, back_populates="projects", lazy="joined"
    )
