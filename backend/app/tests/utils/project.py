import random

from app.schemas.db_schemas import ProjectInBD, ProjectDBCreate
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


def create_random_project_db_create_obj() -> ProjectDBCreate:
    """
    建立測試的 `ProjectDBCreate` model 實例，主要是針對 CRUD 測試時的資料
    """

    title = fake_data.random_string(string_lenght=10)
    max_member_number = fake_data.random_int(1, 10)
    intro = fake_data.random_lorem(nb_sentences=1)
    desc = fake_data.random_lorem(nb_sentences=3)
    image_url = fake_data.random_url()

    project_create = ProjectDBCreate(
        title=title,
        max_member_number=max_member_number,
        intro=intro,
        desc=desc,
        image_url=image_url,
    )

    return project_create
