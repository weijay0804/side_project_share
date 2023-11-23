import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.topic import Topic
from app.tests.utils import utils


def test_create_topic(db: Session) -> None:
    name = utils.fake_data.random_string()

    topic = Topic(name=name)

    db.add(topic)
    db.commit()
    db.refresh(topic)

    assert topic.id is not None
    assert topic.name == name
    assert topic.create_at is not None


def test_create_topic_with_null_name(db: Session) -> None:
    topic = Topic()

    with pytest.raises(IntegrityError):
        db.add(topic)
        db.commit()

    db.rollback()


def test_create_topic_with_same_name(db: Session) -> None:
    name = utils.fake_data.random_string()

    topic1 = Topic(name=name)

    db.add(topic1)
    db.commit()
    db.refresh(topic1)

    topic2 = Topic(name=name)

    with pytest.raises(IntegrityError):
        db.add(topic2)
        db.commit()

    db.rollback()
