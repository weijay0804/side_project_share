from app.schemas.user import UserCreaet
from app.tests.utils.utils import random_email, random_lower_string


def create_random_user_data() -> UserCreaet:
    """建立隨機的使用者資料"""

    email = random_email()
    password = random_lower_string()

    user_in = UserCreaet(username=email, email=email, password=password)

    return user_in
