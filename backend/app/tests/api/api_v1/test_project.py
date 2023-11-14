from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.user import create_random_user_db_create_obj, user_authentication_headers
from app.tests.utils.project import (
    create_random_project_api_create_obj,
    create_random_project_db_create_obj,
)
from app import crud


def test_get_all_project(client: TestClient, db: Session) -> None:
    user_in = create_random_user_db_create_obj()
    user = crud.user.create(db, obj_in=user_in)

    p1_in = create_random_project_db_create_obj()
    p2_in = create_random_project_db_create_obj()

    p1 = crud.project.create(db, user=user, obj_in=p1_in)
    p2 = crud.project.create(db, user=user, obj_in=p2_in)

    r = client.get(f"{settings.API_STR}/projects")

    data = r.json()

    data_title = [d["title"] for d in data]
    data_id = [d["id"] for d in data]

    assert r.status_code == 200
    assert len(data) == 2
    assert p1.title in data_title
    assert p2.title in data_title
    assert p1.id in data_id
    assert p2.id in data_id


def test_get_all_project_with_args(client: TestClient, db: Session) -> None:
    user_in = create_random_user_db_create_obj()
    user = crud.user.create(db, obj_in=user_in)

    p1_in = create_random_project_db_create_obj()
    p2_in = create_random_project_db_create_obj()

    crud.project.create(db, user=user, obj_in=p1_in)
    crud.project.create(db, user=user, obj_in=p2_in)

    r = client.get(f"{settings.API_STR}/projects?limit=1")

    data = r.json()

    assert len(data) == 1


def test_create_project(client: TestClient, db: Session) -> None:
    user_in = create_random_user_db_create_obj()
    crud.user.create(db, obj_in=user_in)

    header = user_authentication_headers(
        client=client, email=user_in.email, password=user_in.password
    )

    paylod = create_random_project_api_create_obj()

    r = client.post(f"{settings.API_STR}/projects", headers=header, json=jsonable_encoder(paylod))

    assert r.status_code == 201


def test_create_project_with_invalid_authentication(client: TestClient, db: Session) -> None:
    invalid_header = {"Authorization": "Bearer invalid"}

    payload = create_random_project_api_create_obj()

    r = client.post(
        f"{settings.API_STR}/projects", headers=invalid_header, json=jsonable_encoder(payload)
    )

    assert r.status_code == 401


def test_get_user_project(client: TestClient, db: Session) -> None:
    user1_in = create_random_user_db_create_obj()
    user2_in = create_random_user_db_create_obj()

    user1 = crud.user.create(db, obj_in=user1_in)
    user2 = crud.user.create(db, obj_in=user2_in)

    p1_in = create_random_project_db_create_obj()
    p2_in = create_random_project_db_create_obj()

    p1 = crud.project.create(db, user=user1, obj_in=p1_in)
    crud.project.create(db, user=user2, obj_in=p2_in)

    header = user_authentication_headers(
        client=client, email=user1_in.email, password=user1_in.password
    )

    r = client.get(f"{settings.API_STR}/projects/me", headers=header)

    data = r.json()

    assert r.status_code == 200
    assert len(data) == 1
    assert data[0]["title"] == p1.title
    assert data[0]["id"] == p1.id


def test_get_user_project_with_invalid_authentication(client: TestClient, db: Session) -> None:
    invalid_header = {"Authorization": "Bearer invalid"}

    r = client.get(f"{settings.API_STR}/projects/me", headers=invalid_header)

    assert r.status_code == 401


def test_get_project(client: TestClient, db: Session) -> None:
    user_in = create_random_user_db_create_obj()
    user = crud.user.create(db, obj_in=user_in)

    p_in = create_random_project_db_create_obj()
    p = crud.project.create(db, user=user, obj_in=p_in)

    r = client.get(f"{settings.API_STR}/projects/{p.id}")

    data = r.json()

    assert r.status_code == 200
    assert data["id"] == p.id
    assert data["title"] == p.title


def test_get_project_with_not_exist_id(client: TestClient, db: Session) -> None:
    r = client.get(f"{settings.API_STR}/projects/10000")

    assert r.status_code == 404


def test_update_project(client: TestClient, db: Session) -> None:
    user_in = create_random_user_db_create_obj()
    user = crud.user.create(db, obj_in=user_in)

    p_in = create_random_project_db_create_obj()
    p = crud.project.create(db, user=user, obj_in=p_in)

    payload = {"max_member_number": 2}

    header = user_authentication_headers(
        client=client, email=user_in.email, password=user_in.password
    )

    r = client.patch(f"{settings.API_STR}/projects/{p.id}", json=payload, headers=header)

    data = r.json()

    assert r.status_code == 200
    assert data["max_member_number"] == 2


def test_update_project_with_invalid_authentication(client: TestClient, db: Session) -> None:
    user_in = create_random_user_db_create_obj()
    user = crud.user.create(db, obj_in=user_in)

    p_in = create_random_project_db_create_obj()
    p = crud.project.create(db, user=user, obj_in=p_in)

    header = {"Authorization": "Bearer invalid"}

    payload = {"title": "test"}

    r = client.patch(f"{settings.API_STR}/projects/{p.id}", json=payload, headers=header)

    assert r.status_code == 401


def test_update_project_with_forbidden_user(client: TestClient, db: Session) -> None:
    user1_in = create_random_user_db_create_obj()
    user1 = crud.user.create(db, obj_in=user1_in)

    user2_in = create_random_user_db_create_obj()
    crud.user.create(db, obj_in=user2_in)

    p_in = create_random_project_db_create_obj()
    p = crud.project.create(db, user=user1, obj_in=p_in)

    header = user_authentication_headers(
        client=client, email=user2_in.email, password=user2_in.password
    )

    payload = {"title": "test"}

    r = client.patch(f"{settings.API_STR}/projects/{p.id}", headers=header, json=payload)

    assert r.status_code == 403
