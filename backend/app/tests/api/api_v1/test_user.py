from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.user import create_random_user_json, create_random_user
from app.tests.utils.utils import FakeData
from app.schemas.user import UserCreaet
from app.crud import user as user_crud


fake = FakeData("zh-TW")


def test_create_user(client: TestClient) -> None:
    user = create_random_user_json()

    data = jsonable_encoder(user)

    r = client.post(f"{settings.API_STR}/users", json=data)

    assert r.status_code == 201


def test_create_user_with_exist_email(client: TestClient, db: Session) -> None:
    user = create_random_user()

    db.add(user)
    db.commit()

    data = {"username": user.username, "email": user.email, "password": "test"}

    r = client.post(f"{settings.API_STR}/users", json=data)

    assert r.status_code == 409


def test_get_user_profile(client: TestClient, db: Session) -> None:
    username = fake.random_username()
    email = fake.random_email()
    password = fake.random_string()

    user_in = UserCreaet(username=username, email=email, password=password)

    user = user_crud.create(db, obj_in=user_in)

    r = client.get(f"{settings.API_STR}/users/{user.id}/profile")

    data = r.json()

    assert r.status_code == 200
    assert data["username"] == user.username
    assert data["email"] == user.email


def test_get_user_profile_with_not_exist_id(client: TestClient) -> None:
    r = client.get(f"{settings.API_STR}/users/10000/profile")

    assert r.status_code == 404


def test_update_user(client: TestClient, db: Session) -> None:
    username = fake.random_username()
    email = fake.random_email()
    password = fake.random_string()

    user_in = UserCreaet(username=username, email=email, password=password)
    user = user_crud.create(db, obj_in=user_in)

    update_data = {"username": "test"}

    r = client.patch(f"{settings.API_STR}/users/{user.id}/profile", json=update_data)

    new_user = user_crud.get(db, user.id)

    assert r.status_code == 200
    assert new_user.username == "test"
    assert new_user.email == user.email


def test_update_user_with_exist_email(client: TestClient, db: Session) -> None:
    username = fake.random_username()
    email = fake.random_email()
    password = fake.random_string()

    user_in = UserCreaet(username=username, email=email, password=password)
    user = user_crud.create(db, obj_in=user_in)

    update_data = {"email": user.email}

    r = client.patch(f"{settings.API_STR}/users/{user.id}/profile", json=update_data)

    assert r.status_code == 409


def test_update_user_with_not_exist_id(client: TestClient) -> None:
    r = client.patch(f"{settings.API_STR}/users/10000/profile", json={"username": "test"})

    assert r.status_code == 404


def test_get_user_proflie_simple(client: TestClient, db: Session) -> None:
    username = fake.random_username()
    email = fake.random_email()
    password = fake.random_string()

    user_in = UserCreaet(username=username, email=email, password=password)
    user = user_crud.create(db, obj_in=user_in)

    r = client.get(f"{settings.API_STR}/users/{user.id}/profile/simple")

    data = r.json()

    assert r.status_code == 200
    assert "username" in data.keys()
    assert "avatar_url" in data.keys()


def test_get_user_profile_simple_with_not_exist_id(client: TestClient) -> None:
    r = client.get(f"{settings.API_STR}/users/1000/profile/simple")

    assert r.status_code == 404