from sqlalchemy.orm import Session

from app import crud
from app.schemas.db_schemas import TopicDBUpdate, TopicDBCreate
from app.tests.utils.project import create_random_project_db_create_obj
from app.tests.utils.user import create_random_user_db_create_obj
from app.tests.utils import utils


def test_create_topic(db: Session) -> None:
    name = utils.fake_data.random_string()
    topic_in = TopicDBCreate(name=name)

    topic = crud.topic.create(db, obj_in=topic_in)

    assert topic.id is not None
    assert topic.name == name


def test_get_topic_by_name(db: Session) -> None:
    name = utils.fake_data.random_string()
    topic_in = TopicDBCreate(name=name)

    topic = crud.topic.create(db, obj_in=topic_in)

    topic_by_name = crud.topic.get_by_name(db, name=name)

    assert topic_by_name == topic
    assert topic_by_name.name == topic.name


def test_update_topic(db: Session) -> None:
    name = utils.fake_data.random_string()

    topic_in = TopicDBCreate(name=name)

    topic = crud.topic.create(db, obj_in=topic_in)

    assert topic.name == name

    update_obj_in = TopicDBUpdate(name="update_topic")

    update_topic = crud.topic.update(db, db_obj=topic, obj_in=update_obj_in)

    assert update_topic.name == "update_topic"


def test_get_topic_projects(db: Session) -> None:
    user_in = create_random_user_db_create_obj()
    user = crud.user.create(db, obj_in=user_in)

    project_in = create_random_project_db_create_obj()
    project = crud.project.create(db, user=user, obj_in=project_in)

    topic1_in = TopicDBCreate(name=utils.fake_data.random_string())
    topic1 = crud.topic.create(db, obj_in=topic1_in)

    topic2_in = TopicDBCreate(name=utils.fake_data.random_string())
    topic2 = crud.topic.create(db, obj_in=topic2_in)

    project.topics.append(topic1)
    project.topics.append(topic2)
    db.commit()

    topic1_project = crud.topic.get_projects(db, topic_id=topic1.id)
    topic2_project = crud.topic.get_projects(db, topic_id=topic2.id)

    assert len(topic1_project) == 1
    assert len(topic2_project) == 1
    assert project in topic1_project
    assert project in topic2_project
