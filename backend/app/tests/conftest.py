from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.db.base import Base


@pytest.fixture(scope="session")
def db() -> Generator:
    engine = create_engine("sqlite:///", connect_args={"check_same_thread": False})

    SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    yield SessionLocal()

    engine.clear_compiled_cache()
    engine.dispose()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
