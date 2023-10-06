import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.encoders import jsonable_encoder

from app.models.project import Project
from app.tests.utils.project import create_random_project_data, create_random_project


def test_create_project(db: Session) -> None:
    """測試建立完整的 project table 資料"""

    project_data = create_random_project_data()

    project = Project(**(jsonable_encoder(project_data)), host_user_id=1)

    db.add(project)
    db.commit()
    db.refresh(project)

    assert project.title == project_data.title
    assert project.host_user_id == 1
    assert project.max_member_number == project_data.max_member_number
    assert project.current_member_number == project_data.current_member_number
    assert project.status == project_data.status
    assert project.intro == project_data.intro
    assert project.desc == project_data.desc
    assert project.image_url == project_data.image_url
    assert project.create_at is not None


def test_project_default(db: Session) -> None:
    """測試 project table 的默認值"""

    title = create_random_project_data().title

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
    """測試新增 project table 資料時沒有 title 欄位資料會引發錯誤"""

    project = Project(host_user_id=1)

    with pytest.raises(IntegrityError):
        db.add(project)
        db.commit()

    db.rollback()


def test_create_project_with_null_host_user_id(db: Session) -> None:
    """測試新增 project table 資料時沒有 host_user_id 欄位資料時會引發錯誤"""

    title = create_random_project_data().title
    project = Project(title=title)

    with pytest.raises(IntegrityError):
        db.add(project)
        db.commit()

    db.rollback()
