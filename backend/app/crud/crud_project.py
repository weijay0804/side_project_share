from typing import Union, Dict, Any, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.project import Project
from app.models.user import User
from app.schemas.db_schemas import ProjectDBCreate, ProjectDBUpdate


class CRUDProject(CRUDBase[Project, ProjectDBCreate, ProjectDBUpdate]):
    def create(self, db: Session, *, user: User, obj_in: ProjectDBCreate) -> Project:
        db_obj = Project(
            title=obj_in.title,
            max_member_number=obj_in.max_member_number,
            intro=obj_in.intro,
            desc=obj_in.desc,
            image_url=obj_in.image_url,
        )

        user.projects.append(db_obj)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def update(
        self, db: Session, *, db_obj: Project, obj_in: Union[ProjectDBUpdate, Dict[str, Any]]
    ) -> Project:
        if isinstance(obj_in, dict):
            update_data = obj_in

        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_user_projects(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 10
    ) -> List[Project]:
        """取得屬於特定使用者的 project list"""

        projects = (
            db.query(self.model)
            .filter(Project.host_user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

        return projects


project = CRUDProject(Project)
