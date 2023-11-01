"""

使用者相關路由

以下的 endpoint 會以 "<api_prefix>/user" 開頭

"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import api_schemas
from app import crud
from app.api import deps
from app.models import User


router = APIRouter()


@router.post("/", status_code=201, summary="新增一個使用者")
def create_user(item: api_schemas.UserCreate, db: Session = Depends(deps.get_db)):
    """新增使用者"""

    user_by_email = crud.user.get_by_email(db, email=item.email)

    if user_by_email:
        raise HTTPException(status_code=409, detail="The email is exist.")

    db_user = crud.user.create(db, obj_in=item)

    return {"message": "ok", "user_id": db_user.id}


@router.get("/me/profile", summary="取得詳細的使用者個人資料", response_model=api_schemas.User)
def get_user_profile(user: User = Depends(deps.get_current_user)):
    """取得用戶個人資料"""

    return user


@router.patch("/me/profile", summary="更新使用者個人資料", response_model=api_schemas.User)
def update_user_profile(
    item: api_schemas.UserUpdate,
    user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    """更新用戶個人資料"""

    if item.email:
        user_by_email = crud.user.get_by_email(db, email=item.email)

        if user_by_email:
            raise HTTPException(status_code=409, detail="The email is exist")

    new_user = crud.user.update(db, db_obj=user, obj_in=item)

    return new_user


@router.get(
    "/{user_id}/profile/simple", summary="取得簡易的使用者個人資料", response_model=api_schemas.UserSimple
)
def get_user_profile_simple(user_id: int, db: Session = Depends(deps.get_db)):
    """取得簡易版的用戶個人資料"""

    db_user = crud.user.get(db, user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail=f"Can't found user id: {user_id}.")

    return db_user
