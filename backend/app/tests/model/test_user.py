import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.encoders import jsonable_encoder

from app.models.user import User
from app.tests.utils.user import create_random_user_data


def test_create_user(db: Session) -> None:
    """測試建立完整的 user table 資料"""

    user_in = create_random_user_data()

    user = User(**(jsonable_encoder(user_in)), password="test")

    db.add(user)
    db.commit()
    db.refresh(user)

    assert user.id is not None
    assert user.username == user_in.username
    assert user.email == user_in.email
    assert user.password_hash is not None
    assert user.avatar_url == user_in.avatar_url
    assert user.city == user_in.city
    assert user.age == user_in.age
    assert user.gender == user_in.gender
    assert user.is_email_public == user_in.is_email_public
    assert user.github == user_in.github
    assert user.is_github_public == user_in.is_github_public
    assert user.discord == user_in.discord
    assert user.is_discord_public == user_in.is_discord_public
    assert user.skill == user_in.skill
    assert user.create_at is not None


def test_user_default(db: Session) -> None:
    """測試 user table 的默認值"""

    user_data = create_random_user_data()

    user = User(username=user_data.username, email=user_data.email)

    db.add(user)
    db.commit()
    db.refresh(user)

    assert user.id is not None
    assert user.username == user_data.username
    assert user.email == user_data.email
    assert user.password_hash is None
    assert user.avatar_url is None
    assert user.city is None
    assert user.age is None
    assert user.gender is None
    assert user.is_email_public is False
    assert user.github is None
    assert user.is_github_public is False
    assert user.discord is None
    assert user.is_discord_public is False
    assert user.skill is None
    assert user.create_at is not None


def test_create_user_with_same_username(db: Session) -> None:
    """測試 username 欄位的唯一性"""

    user_in = create_random_user_data()

    user = User(**(jsonable_encoder(user_in)))

    db.add(user)
    db.commit()

    user_in2 = create_random_user_data()
    user2 = User(username=user_in.username, email=user_in2.email)

    with pytest.raises(IntegrityError):
        db.add(user2)
        db.commit()

    db.rollback()


def test_create_user_with_same_email(db: Session) -> None:
    """測試 email 欄位的唯一性"""

    user_in = create_random_user_data()

    user = User(**(jsonable_encoder(user_in)))

    db.add(user)
    db.commit()

    user_in2 = create_random_user_data()
    user2 = User(username=user_in2.username, email=user_in.email)

    with pytest.raises(IntegrityError):
        db.add(user2)
        db.commit()

    db.rollback()


def test_create_user_with_null_username(db: Session) -> None:
    """測試建立 user table 資料時，沒有 username 欄位資料會引發錯誤"""

    user_in = create_random_user_data()

    user = User(email=user_in.email)

    with pytest.raises(IntegrityError):
        db.add(user)
        db.commit()

    db.rollback()


def test_create_user_with_null_email(db: Session) -> None:
    """測試建立 user table 資料時，沒有 email 欄位資料會引發錯誤"""

    user_in = create_random_user_data()

    user = User(username=user_in.username)

    with pytest.raises(IntegrityError):
        db.add(user)
        db.commit()

    db.rollback()
