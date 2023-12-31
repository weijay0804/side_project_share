"""

專案計畫相關路由

"""

from typing import Optional, List

from fastapi import APIRouter, Query, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.schemas import api_schemas
from app.schemas import db_schemas
from app import crud
from app.api import deps
from app.models import User

router = APIRouter()


@router.get("/", summary="取得所有的專案計畫資料", response_model=List[api_schemas.ProjectSimple])
def get_all_project(
    db: Session = Depends(deps.get_db),
    skip: Optional[int] = Query(default=0, ge=1),
    limit: Optional[int] = Query(default=10, ge=1, le=10, description="一次回傳的專案數量"),
):
    """取得所有的專案資料"""

    projcets = crud.project.get_multi(db, skip=skip, limit=limit)

    result = []

    for p in projcets:
        tmp = api_schemas.ProjectSimple(
            **(jsonable_encoder(p)),
            host_username=p.user.username,
            host_user_avatar_url=p.user.avatar_url,
            topic=[],
        )

        result.append(tmp)

    return result


@router.post("/", summary="新增一個專案計畫", response_model=api_schemas.ProjectSimple, status_code=201)
def create_project(
    item: api_schemas.ProjectCreate,
    db: Session = Depends(deps.get_db),
    user: User = Depends(deps.get_current_user),
):
    """新增專案"""

    project_in = db_schemas.ProjectDBCreate(
        title=item.title,
        max_member_number=item.max_member_number,
        intro=item.intro,
        desc=item.desc,
        image_url=item.image_url,
    )

    project = crud.project.create(db, user=user, obj_in=project_in)

    return api_schemas.ProjectSimple(
        **(jsonable_encoder(project)),
        host_username=user.username,
        host_user_avatar_url=user.avatar_url,
    )


@router.get("/me", summary="取得所有屬於使用者自己的專案計畫", response_model=List[api_schemas.ProjectMe])
def get_user_project(
    db: Session = Depends(deps.get_db),
    user: User = Depends(deps.get_current_user),
    skip: Optional[int] = Query(default=0, ge=1),
    limit: Optional[int] = Query(default=10, ge=1, le=10, description="一次回傳的專案數量"),
):
    """取得使用者的專案資料"""

    projcets = crud.project.get_user_projects(db, user_id=user.id, skip=skip, limit=limit)

    result = []

    for p in projcets:
        tmp = api_schemas.ProjectMe(id=p.id, title=p.title, status=p.status, topic=[])

        result.append(tmp)

    return result


@router.get("/{project_id}", summary="取得指定專案計畫的詳細資料", response_model=api_schemas.Project)
def get_project(project_id: int, db: Session = Depends(deps.get_db)):
    """取得專案的詳細資料"""

    project = crud.project.get(db, project_id)

    if project is None:
        raise HTTPException(status_code=404, detail=f"Project ID {project_id} is not exist.")

    result = api_schemas.Project(
        **(jsonable_encoder(project)),
        host_username=project.user.username,
        host_user_avatar_url=project.user.avatar_url,
        topic=[],
        member=[],
    )

    return result


@router.patch("/{project_id}", summary="更新專案資料", response_model=api_schemas.Project)
def update_project(
    project_id: int,
    item: api_schemas.ProjectUpdate,
    db: Session = Depends(deps.get_db),
    user: User = Depends(deps.get_current_user),
):
    project = crud.project.get(db, project_id)

    if project is None:
        raise HTTPException(status_code=404, detail="Project is not exist.")

    if project.user.id != user.id:
        raise HTTPException(status_code=403, detail="No Permissions.")

    project_in = db_schemas.ProjectDBUpdate(**(jsonable_encoder(item)))

    new_project = crud.project.update(db, db_obj=project, obj_in=project_in)

    return api_schemas.Project(
        **jsonable_encoder(new_project),
        host_username=project.user.username,
        host_user_avatar_url=project.user.avatar_url,
    )
