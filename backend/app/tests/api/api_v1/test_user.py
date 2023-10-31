from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.user import create_random_user_create_obj, user_authentication_headers
from app.crud import user as user_crud


def test_create_user(client: TestClient) -> None:
    user = create_random_user_create_obj()

    data = jsonable_encoder(user)

    r = client.post(f"{settings.API_STR}/users", json=data)

    assert r.status_code == 201


def test_create_user_with_exist_email(client: TestClient, db: Session) -> None:
    user_in = create_random_user_create_obj()

    user = user_crud.create(db, obj_in=user_in)

    data = {"username": user.username, "email": user.email, "password": "test"}

    r = client.post(f"{settings.API_STR}/users", json=data)

    assert r.status_code == 409


def test_get_user_profile(client: TestClient, db: Session) -> None:
    user_in = create_random_user_create_obj()

    user = user_crud.create(db, obj_in=user_in)

    headers = user_authentication_headers(
        client=client, email=user_in.email, password=user_in.password
    )

    r = client.get(f"{settings.API_STR}/users/me/profile", headers=headers)

    data = r.json()

    assert r.status_code == 200
    assert data["username"] == user.username
    assert data["email"] == user.email


def test_get_user_profile_with_invalid_authentication(client: TestClient) -> None:
    invalid_header = {"Authorization": "Bearer invalid"}

    r = client.get(f"{settings.API_STR}/users/me/profile", headers=invalid_header)

    assert r.status_code == 401


def test_update_user(client: TestClient, db: Session) -> None:
    user_in = create_random_user_create_obj()
    user = user_crud.create(db, obj_in=user_in)

    headers = user_authentication_headers(
        client=client, email=user_in.email, password=user_in.password
    )

    update_data = {"username": "test"}

    r = client.patch(f"{settings.API_STR}/users/me/profile", json=update_data, headers=headers)

    new_user = user_crud.get(db, user.id)

    assert r.status_code == 200
    assert new_user.username == "test"
    assert new_user.email == user.email


def test_update_user_with_invalid_authentication(client: TestClient) -> None:
    invalid_header = {"Authorization": "Bearer invalid"}

    r = client.patch(
        f"{settings.API_STR}/users/me/profile", json={"username": "test"}, headers=invalid_header
    )

    assert r.status_code == 401


def test_update_user_with_exist_email(client: TestClient, db: Session) -> None:
    user_in = create_random_user_create_obj()
    user = user_crud.create(db, obj_in=user_in)

    headers = user_authentication_headers(
        client=client, email=user_in.email, password=user_in.password
    )

    update_data = {"email": user.email}

    r = client.patch(f"{settings.API_STR}/users/me/profile", json=update_data, headers=headers)

    assert r.status_code == 409


def test_get_user_proflie_simple(client: TestClient, db: Session) -> None:
    user_in = create_random_user_create_obj()
    user = user_crud.create(db, obj_in=user_in)

    r = client.get(f"{settings.API_STR}/users/{user.id}/profile/simple")

    data = r.json()

    assert r.status_code == 200
    assert "username" in data.keys()
    assert "avatar_url" in data.keys()


def test_get_user_profile_simple_with_not_exist_id(client: TestClient) -> None:
    r = client.get(f"{settings.API_STR}/users/1000/profile/simple")

    assert r.status_code == 404
