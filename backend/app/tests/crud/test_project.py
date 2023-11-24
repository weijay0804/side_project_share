from sqlalchemy.orm import Session

from app import crud
from app.schemas.db_schemas import ProjectDBUpdate, TopicDBCreate
from app.tests.utils.user import create_random_user_db_create_obj
from app.tests.utils.project import create_random_project_db_create_obj
from app.tests.utils import utils


def test_create_project(db: Session) -> None:
    user_in = create_random_user_db_create_obj()
    user = crud.user.create(db, obj_in=user_in)

    project_in = create_random_project_db_create_obj()

    project = crud.project.create(db, user=user, obj_in=project_in)

    assert project.id is not None
    assert project.title == project_in.title
    assert project.max_member_number == project_in.max_member_number
    assert project.current_member_number == 0
    assert project.intro == project_in.intro
    assert project.desc == project_in.desc
    assert project.image_url == project_in.image_url


def test_update_project(db: Session) -> None:
    user_in = create_random_user_db_create_obj()
    user = crud.user.create(db, obj_in=user_in)

    project_in = create_random_project_db_create_obj()
    project = crud.project.create(db, user=user, obj_in=project_in)

    assert project.title == project_in.title

    update_data = ProjectDBUpdate(title="update_test")

    updated_project = crud.project.update(db, db_obj=project, obj_in=update_data)

    assert updated_project.title == "update_test"
    assert updated_project.max_member_number == project.max_member_number
    assert updated_project.desc == project.desc


def test_get_user_projects(db: Session) -> None:
    user_in = create_random_user_db_create_obj()
    user = crud.user.create(db, obj_in=user_in)

    project1_in = create_random_project_db_create_obj()
    project1 = crud.project.create(db, user=user, obj_in=project1_in)

    project2_in = create_random_project_db_create_obj()
    project2 = crud.project.create(db, user=user, obj_in=project2_in)

    user_projects = crud.project.get_user_projects(db, user_id=user.id)

    assert len(user_projects) == 2
    assert project1 in user_projects
    assert project2 in user_projects


def test_add_topic(db: Session) -> None:
    user_in = create_random_user_db_create_obj()
    user = crud.user.create(db, obj_in=user_in)

    project_in = create_random_project_db_create_obj()
    project = crud.project.create(db, user=user, obj_in=project_in)

    topics = project.topics

    assert topics == []

    topic_in = TopicDBCreate(name=utils.fake_data.random_string())
    topic = crud.topic.create(db, obj_in=topic_in)

    crud.project.add_topic(db, db_obj=project, topic=topic)

    topics = project.topics

    assert len(topics) == 1
    assert topic in topics


def test_get_topics(db: Session) -> None:
    user_in = create_random_user_db_create_obj()
    user = crud.user.create(db, obj_in=user_in)

    project_in = create_random_project_db_create_obj()
    project = crud.project.create(db, user=user, obj_in=project_in)

    topic_in = TopicDBCreate(name=utils.fake_data.random_string())
    topic = crud.topic.create(db, obj_in=topic_in)

    project.topics.append(topic)
    db.commit()

    topics = crud.project.get_topics(db_obj=project)

    assert len(topics) == 1
    assert topic in topics
