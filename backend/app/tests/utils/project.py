import random

from fastapi.encoders import jsonable_encoder

from app.models.project import Project
from app.schemas.project import ProjectInBD
from app.tests.utils.utils import FakeData


fake = FakeData(locale="zh_TW")


def create_random_project_data() -> ProjectInBD:
    """建立測試用 Project 資料"""

    project_model = ProjectInBD(
        title=fake.random_string(20),
        max_member_number=fake.random_int(5, 10),
        current_member_number=fake.random_int(1, 4),
        status=random.choice(["recruit", "progress", "done"]),
        intro=fake.random_string(30),
        desc=fake.random_lorem(),
        image_url=fake.random_url(),
    )

    return project_model


def create_random_project(host_user_id: int) -> Project:
    """建立測試用的 Project model 實例"""

    project = Project(**(jsonable_encoder(create_random_project_data())), host_user_id=host_user_id)

    return project
