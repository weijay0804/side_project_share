from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


from app.tests.utils.user import create_random_user_db_create_obj
from app.core.config import settings
from app import crud


def test_login_for_access_token(client: TestClient, db: Session) -> None:
    user_in = create_random_user_db_create_obj()
    crud.user.create(db, obj_in=user_in)

    data = {"username": user_in.email, "password": user_in.password}

    r = client.post(f"{settings.API_STR}/auth/token", data=data)
    r_data = r.json()

    assert r.status_code == 200
    assert r_data["access_token"] is not None
    assert r_data["token_type"] == "bearer"


def test_login_for_access_token_invalid_email(client: TestClient, db: Session) -> None:
    user_in = create_random_user_db_create_obj()
    crud.user.create(db, obj_in=user_in)

    data = {"username": "invalid_email", "password": user_in.password}

    r = client.post(f"{settings.API_STR}/auth/token", data=data)

    assert r.status_code == 401


def test_login_for_access_token_invalid_password(client: TestClient, db: Session) -> None:
    user_in = create_random_user_db_create_obj()
    crud.user.create(db, obj_in=user_in)

    data = {"username": user_in.email, "password": "invalid_password"}

    r = client.post(f"{settings.API_STR}/auth/token", data=data)

    assert r.status_code == 401
