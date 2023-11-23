from sqlalchemy import Table, Column, Integer, ForeignKey

from app.db.base_class import Base

project_topic_table = Table(
    "project_topic_intermediay",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("project.id"), primary_key=True),
    Column("topic_id", Integer, ForeignKey("topic.id"), primary_key=True),
)
