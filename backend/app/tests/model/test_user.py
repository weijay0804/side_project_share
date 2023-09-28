import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.encoders import jsonable_encoder

from app.models.user import User
from app.tests.utils.user import create_random_user_data


def test_create_user(db: Session) -> None:
    user_in = create_random_user_data()

    user = User(**(jsonable_encoder(user_in)))

    db.add(user)
    db.commit()

    db_user = db.query(User).filter(User.username == user_in.username).first()

    assert db_user.username == user_in.username
    assert db_user.email == user_in.email
    assert db_user.avatar_url is None
    assert db_user.city is None
    assert db_user.age is None
    assert db_user.gender is None
    assert db_user.is_email_public is False
    assert db_user.github is None
    assert db_user.is_github_public is False
    assert db_user.discord is None
    assert db_user.is_discord_public is False
    assert db_user.skill is None
    assert db_user.create_at is not None


def test_create_user_with_same_username(db: Session) -> None:
    user_in = create_random_user_data()

    user = User(**(jsonable_encoder(user_in)))

    db.add(user)
    db.commit()

    user_in2 = create_random_user_data()
    user2 = User(username=user_in.username, email=user_in2.email, password=user_in2.password)

    with pytest.raises(IntegrityError):
        db.add(user2)
        db.commit()

    db.rollback()


def test_create_user_with_same_email(db: Session) -> None:
    user_in = create_random_user_data()

    user = User(**(jsonable_encoder(user_in)))

    db.add(user)
    db.commit()

    user_in2 = create_random_user_data()
    user2 = User(username=user_in2.username, email=user_in.email, password=user_in2.password)

    with pytest.raises(IntegrityError):
        db.add(user2)
        db.commit()

    db.rollback()


def test_create_user_with_null_username(db: Session) -> None:
    user_in = create_random_user_data()

    user = User(email=user_in.email, password=user_in.password)

    with pytest.raises(IntegrityError):
        db.add(user)
        db.commit()

    db.rollback()


def test_create_user_with_null_email(db: Session) -> None:
    user_in = create_random_user_data()

    user = User(username=user_in.username, password=user_in.password)

    with pytest.raises(IntegrityError):
        db.add(user)
        db.commit()

    db.rollback()
