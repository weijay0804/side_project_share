from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app import crud
from app.core.security import verify_password
from app.schemas.user import UserCreaet, UserUpdate
from app.tests.utils.utils import FakeData

FD = FakeData("zh-TW")


def test_create_user(db: Session) -> None:
    email = FD.random_email()
    username = FD.random_username()
    password = FD.random_string()

    user_in = UserCreaet(username=username, email=email, password=password)
    user = crud.user.create(db, obj_in=user_in)

    assert user.username == username
    assert user.email == email
    assert hasattr(user, "password_hash")


def test_authenticate_user(db: Session) -> None:
    email = FD.random_email()
    username = FD.random_username()
    password = FD.random_string()

    user_in = UserCreaet(username=username, email=email, password=password)

    user = crud.user.create(db, obj_in=user_in)
    authenticated_user = crud.user.authenticate(db, email=email, password=password)

    assert authenticated_user
    assert authenticated_user.email == user.email


def test_not_authenticate_user(db: Session) -> None:
    email = FD.random_email()
    password = FD.random_string()

    user = crud.user.authenticate(db, email=email, password=password)

    assert user is None


def test_get_user_by_email(db: Session) -> None:
    username = FD.random_username()
    email = FD.random_email()
    password = FD.random_string()

    user_in = UserCreaet(username=username, email=email, password=password)

    user = crud.user.create(db, obj_in=user_in)

    user_get = crud.user.get_by_username(db, username=username)

    assert user_get
    assert user_get.username == user.username
    assert user_get.email == user.email
    assert jsonable_encoder(user_get) == jsonable_encoder(user)


def test_get_user_by_username(db: Session) -> None:
    username = FD.random_username()
    email = FD.random_email()
    password = FD.random_string()

    user_in = UserCreaet(username=username, email=email, password=password)
    user = crud.user.create(db, obj_in=user_in)

    user_get = crud.user.get_by_username(db, username=username)

    assert user_get
    assert user_get.email == user.email
    assert user_get.username == user.username
    assert jsonable_encoder(user_get) == jsonable_encoder(user)


def test_get_user(db: Session) -> None:
    username = FD.random_username()
    email = FD.random_email()
    password = FD.random_string()

    user_in = UserCreaet(username=username, email=email, password=password)

    user = crud.user.create(db, obj_in=user_in)

    user_get = crud.user.get(db, user.id)

    assert user_get
    assert user_get.username == user.username
    assert jsonable_encoder(user_get) == jsonable_encoder(user)


def test_update_user(db: Session) -> None:
    username = FD.random_username()
    email = FD.random_email()
    password = FD.random_string()

    user_in = UserCreaet(username=username, email=email, password=password)

    user = crud.user.create(db, obj_in=user_in)

    new_password = FD.random_string()
    user_in_update = UserUpdate(password=new_password)

    crud.user.update(db, db_obj=user, obj_in=user_in_update)

    user_updated = crud.user.get(db, id=user.id)

    assert user_updated
    assert user.email == user_updated.email
    assert verify_password(new_password, user_updated.password_hash)
