import random

from fastapi.encoders import jsonable_encoder

from app.models.user import User
from app.schemas.user import UserInDB
from app.tests.utils.utils import FakeData

fake = FakeData("zh_TW")


def create_random_user_data() -> UserInDB:
    """建立隨機的使用者資料"""

    def random_true_false() -> bool:
        return random.choice([True, False])

    user_in = UserInDB(
        username=fake.random_username(),
        email=fake.random_email(),
        avatar_url=fake.random_url(),
        city=fake.random_city(),
        age=fake.random_int(10, 60),
        gender=random.choice(["male", "female", "sex"]),
        is_email_public=random_true_false(),
        github=fake.random_email(),
        is_github_public=random_true_false(),
        discord=fake.random_email(),
        is_discord_public=random_true_false(),
        skill=fake.random_lorem(),
    )

    return user_in


def create_random_user(is_password: bool = True) -> User:
    """建立測試的 User model 實例"""

    user = User(
        **(jsonable_encoder(create_random_user_data())),
        password=fake.random_string() if is_password else None
    )

    return user
