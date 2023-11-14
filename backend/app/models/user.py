from datetime import datetime

from sqlalchemy import Column, Integer, String, SmallInteger, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from passlib.context import CryptContext

from app.db.base_class import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), index=True, nullable=False)
    email = Column(String(128), index=True, unique=True, nullable=False)
    password_hash = Column(String(128))
    avatar_url = Column(Text)
    city = Column(String)
    age = Column(SmallInteger)
    gender = Column(String(15))
    is_email_public = Column(Boolean(), default=False)
    github = Column(String(128))
    is_github_public = Column(Boolean(), default=False)
    discord = Column(String(128))
    is_discord_public = Column(Boolean(), default=False)
    skill = Column(Text)
    create_at = Column(DateTime, default=datetime.utcnow)

    # 建立與 project table 一對多的關係
    projects = relationship(
        "Project", back_populates="user", cascade="delete, delete-orphan", lazy="dynamic"
    )
