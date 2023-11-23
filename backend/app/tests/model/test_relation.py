from typing import Generator

import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.models.user import User
from app.models.project import Project
from app.models.topic import Topic
from app.tests.utils import utils
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


@pytest.fixture(scope="function")
def clear_topic(db: Session) -> Generator:
    yield None

    db.execute(text("DELETE FROM topic"))
    db.commit()


@pytest.fixture(scope="function")
def clear_project_topic_intermediary(db: Session) -> Generator:
    yield None

    db.execute(text("DELETE FROM project_topic_intermediay"))
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


@pytest.mark.usefixtures("clear_project_topic_intermediary")
@pytest.mark.usefixtures("clear_project")
@pytest.mark.usefixtures("clear_topic")
@pytest.mark.usefixtures("db_user")
class TestProjectTopicRelation:
    def test_create(self, db: Session, db_user: User) -> None:
        project_data = create_random_project_data()
        project = Project(**jsonable_encoder(project_data), host_user_id=db_user.id)

        topic = Topic(name=utils.fake_data.random_string())

        db.add_all([project, topic])
        db.commit()
        db.refresh(project)
        db.refresh(topic)

        project_topic = project.topics

        assert len(project_topic) == 0

        project.topics.append(topic)

        db.commit()

        project_topic = project.topics

        assert len(project_topic) == 1
        assert topic == project_topic[0]

    def test_create_many_topic(self, db: Session, db_user: User) -> None:
        project_data = create_random_project_data()
        project = Project(**jsonable_encoder(project_data), host_user_id=db_user.id)

        topic1 = Topic(name=utils.fake_data.random_string())
        topic2 = Topic(name=utils.fake_data.random_string())

        db.add_all([project, topic1, topic2])
        db.commit()
        db.refresh(project)
        db.refresh(topic1)
        db.refresh(topic2)

        project.topics.append(topic1)
        project.topics.append(topic2)

        db.commit()

        project_topic = project.topics

        assert len(project_topic) == 2
        assert topic1 in project_topic
        assert topic2 in project_topic

    def test_create_many_project(self, db: Session, db_user: User) -> None:
        project1_data = create_random_project_data()
        project2_data = create_random_project_data()

        project1 = Project(**jsonable_encoder(project1_data), host_user_id=db_user.id)
        project2 = Project(**jsonable_encoder(project2_data), host_user_id=db_user.id)

        topic = Topic(name=utils.fake_data.random_string())

        db.add_all([project1, project2, topic])
        db.commit()
        db.refresh(project1)
        db.refresh(project2)
        db.refresh(topic)

        project1.topics.append(topic)
        project2.topics.append(topic)
        db.commit()

        project1_topic = project1.topics
        project2_topic = project2.topics

        assert len(project1_topic) == 1
        assert len(project2_topic) == 1
        assert topic in project1_topic
        assert topic in project2_topic

    def test_remove_topic(self, db: Session, db_user: User) -> None:
        project_data = create_random_project_data()
        project = Project(**jsonable_encoder(project_data), host_user_id=db_user.id)

        topic = Topic(name=utils.fake_data.random_string())

        db.add_all([project, topic])
        db.commit()
        db.refresh(project)
        db.refresh(topic)

        project.topics.append(topic)
        db.commit()

        project_topic = project.topics

        assert topic in project_topic

        project.topics.remove(topic)
        db.commit()

        project_topic = project.topics

        assert topic not in project_topic

    def test_delete_project(self, db: Session, db_user: User) -> None:
        project_data = create_random_project_data()
        project = Project(**jsonable_encoder(project_data), host_user_id=db_user.id)

        topic = Topic(name=utils.fake_data.random_string())

        db.add_all([project, topic])
        db.commit()
        db.refresh(project)
        db.refresh(topic)

        project.topics.append(topic)
        db.commit()

        db.delete(project)
        db.commit()

        project = db.get(Project, project.id)
        topic = db.get(Topic, topic.id)
        topic_project = topic.projects.all()

        assert project is None
        assert topic is not None
        assert len(topic_project) == 0

    def test_delete_topic(self, db: Session, db_user: User) -> None:
        project_data = create_random_project_data()
        project = Project(**jsonable_encoder(project_data), host_user_id=db_user.id)

        topic = Topic(name=utils.fake_data.random_string())

        db.add_all([project, topic])
        db.commit()
        db.refresh(project)
        db.refresh(topic)

        project.topics.append(topic)
        db.commit()

        db.delete(topic)
        db.commit()

        topic = db.get(Topic, topic.id)
        project = db.get(Project, project.id)

        project_topic = project.topics

        assert topic is None
        assert project is not None
        assert len(project_topic) == 0
