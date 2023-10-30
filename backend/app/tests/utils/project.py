import random

from fastapi.encoders import jsonable_encoder

from app.schemas.project import ProjectInBD
from app.tests.utils.utils import fake_data


def create_random_project_data() -> ProjectInBD:
    """建立測試用 Project 資料"""

    project_model = ProjectInBD(
        title=fake_data.random_string(20),
        max_member_number=fake_data.random_int(5, 10),
        current_member_number=fake_data.random_int(1, 4),
        status=random.choice(["recruit", "progress", "done"]),
        intro=fake_data.random_string(30),
        desc=fake_data.random_lorem(),
        image_url=fake_data.random_url(),
    )

    return project_model
