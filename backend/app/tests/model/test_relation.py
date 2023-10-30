from typing import Generator

import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.models.user import User
from app.models.project import Project
from app.tests.utils.user import create_random_user_data
from app.tests.utils.project import create_random_project_data


@pytest.fixture(scope="class")
def db_user(db: Session) -> User:
    """取得 user object"""

    user_in = create_random_user_data()

    user = User(**(jsonable_encoder(user_in)))

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@pytest.fixture(scope="function")
def clear_project(db: Session) -> Generator:
    """清理 project table"""

    yield None
    db.execute(text("DELETE FROM project"))
    db.commit()


@pytest.mark.usefixtures("clear_project")
@pytest.mark.usefixtures("db_user")
class TestUserProjectRelation:
    def test_create(self, db: Session, db_user: User) -> None:
        """測試專案與使用者之間的關聯"""

        project_data = create_random_project_data()
        project = Project(**jsonable_encoder(project_data), host_user_id=db_user.id)

        db.add(project)
        db.commit()
        db.refresh(project)

        user_project = db_user.projects.all()

        assert len(user_project) == 1
        assert user_project[0] == project
        assert project.user == db_user

    def test_create_many(self, db: Session, db_user: User) -> None:
        """測試多個專案與使用者之間的關聯"""

        project1_data = create_random_project_data()
        project2_data = create_random_project_data()

        project1 = Project(**jsonable_encoder(project1_data), host_user_id=db_user.id)
        project2 = Project(**jsonable_encoder(project2_data), host_user_id=db_user.id)

        db.add_all([project1, project2])
        db.commit()

        user_project = db_user.projects.all()

        assert len(user_project) == 2
        assert project1 in user_project
        assert project2 in user_project

    def test_delete_project(self, db: Session, db_user: User) -> None:
        """測試刪除專案時不應該刪除使用者"""

        project_data = create_random_project_data()
        project = Project(**jsonable_encoder(project_data), host_user_id=db_user.id)

        db.add(project)
        db.commit()
        db.refresh(project)

        user = db.get(User, db_user.id)

        assert user is not None

        db.delete(project)
        db.commit()

        deleted_project = db.get(Project, project.id)

        assert deleted_project is None

        user = db.get(User, db_user.id)

        assert user is not None

    def test_delete_user(self, db: Session) -> None:
        """測試刪除使用者時，關聯的專案也要一起刪除"""

        user = User(**(jsonable_encoder(create_random_user_data())))

        db.add(user)
        db.commit()
        db.refresh(user)

        project1_data = create_random_project_data()
        project2_data = create_random_project_data()

        project1 = Project(**jsonable_encoder(project1_data), host_user_id=user.id)
        project2 = Project(**jsonable_encoder(project2_data), host_user_id=user.id)

        db.add_all([project1, project2])
        db.commit()
        db.refresh(project1)
        db.refresh(project2)

        db.delete(user)
        db.commit()

        deleted_user = db.get(User, user.id)

        assert deleted_user is None

        deleted_project1 = db.get(Project, project1.id)
        deleted_project2 = db.get(Project, project2.id)

        assert deleted_project1 is None
        assert deleted_project2 is None
