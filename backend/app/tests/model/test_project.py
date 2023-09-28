import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.encoders import jsonable_encoder

from app.models.project import Project
from app.tests.utils.utils import random_lower_string


def test_create_project(db: Session) -> None:
    title = random_lower_string()

    project = Project(title=title, host_user_id=1)

    db.add(project)
    db.commit()
    db.refresh(project)

    assert project.title == title
    assert project.host_user_id == 1
    assert project.max_member_number == 10
    assert project.current_member_number == 0
    assert project.status == "recruit"
    assert project.intro is None
    assert project.desc is None
    assert project.image_url is None
    assert project.create_at is not None


def test_create_project_with_null_title(db: Session) -> None:
    project = Project(host_user_id=1)

    with pytest.raises(IntegrityError):
        db.add(project)
        db.commit()

    db.rollback()


def test_create_project_with_null_host_user_id(db: Session) -> None:
    project = Project(title=random_lower_string())

    with pytest.raises(IntegrityError):
        db.add(project)
        db.commit()

    db.rollback()
