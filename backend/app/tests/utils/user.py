from typing import Dict
import random

from fastapi.testclient import TestClient

from app.schemas.user import UserInDB, UserCreaet
from app.tests.utils.utils import fake_data
from app.core.config import settings


def create_random_user_data() -> UserInDB:
    """建立隨機的使用者資料"""

    def random_true_false() -> bool:
        return random.choice([True, False])

    user_in = UserInDB(
        username=fake_data.random_username(),
        email=fake_data.random_email(),
        avatar_url=fake_data.random_url(),
        city=fake_data.random_city(),
        age=fake_data.random_int(10, 60),
        gender=random.choice(["male", "female", "sex"]),
        is_email_public=random_true_false(),
        github=fake_data.random_email(),
        is_github_public=random_true_false(),
        discord=fake_data.random_email(),
        is_discord_public=random_true_false(),
        skill=fake_data.random_lorem(),
    )

    return user_in


def create_random_user_create_obj() -> UserCreaet:
    """建立測試的 UserCreate model 實例"""

    username = fake_data.random_username()
    email = fake_data.random_email()
    password = fake_data.random_string()

    user_create = UserCreaet(username=username, email=email, password=password)

    return user_create


def user_authentication_headers(*, client: TestClient, email: str, password: str) -> Dict[str, str]:
    """認證使用者，並回傳 Bearer headers"""

    data = {"username": email, "password": password}

    r = client.post(f"{settings.API_STR}/auth/token", data=data)

    token = r.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    return headers
