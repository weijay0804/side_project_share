from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.main import app
from app.db.base import Base
from app.api import deps


@pytest.fixture(scope="module")
def db() -> Generator:
    engine = create_engine(
        "sqlite:///", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )

    SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    session = SessionLocal()

    try:
        yield session

    finally:
        session.close()
        engine.clear_compiled_cache()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def client(db: Session):
    def _get_test_db():
        yield db

    with TestClient(app) as c:
        app.dependency_overrides[deps.get_db] = _get_test_db
        yield c
