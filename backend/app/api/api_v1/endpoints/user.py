"""

使用者相關路由

以下的 endpoint 會以 "<api_prefix>/user" 開頭

"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app import crud


router = APIRouter()


@router.post("/", status_code=201, summary="新增一個使用者")
def create_user(item: schemas.UserCreaet, db: Session = Depends(deps.get_db)):
    """新增使用者"""

    user_by_email = crud.user.get_by_email(db, email=item.email)

    if user_by_email:
        raise HTTPException(status_code=409, detail="The email is exist.")

    db_user = crud.user.create(db, obj_in=item)

    return {"message": "ok", "user_id": db_user.id}


@router.get("/{user_id}/profile", summary="取得詳細的使用者個人資料", response_model=schemas.User)
def get_user_profile(user_id: int, db: Session = Depends(deps.get_db)):
    """取得用戶個人資料"""

    db_user = crud.user.get(db, user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail=f"Can't found user id: {user_id}.")

    return db_user


@router.patch("/{user_id}/profile", summary="更新使用者個人資料", response_model=schemas.User)
def update_user_profile(user_id: int, item: schemas.UserUpdate, db: Session = Depends(deps.get_db)):
    """更新用戶個人資料"""

    if item.email:
        user_by_email = crud.user.get_by_email(db, email=item.email)

        if user_by_email:
            raise HTTPException(status_code=409, detail="The email is exist")

    db_user = crud.user.get(db, user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail=f"Can't found user id: {user_id}")

    new_user = crud.user.update(db, db_obj=db_user, obj_in=item)

    return new_user


@router.get("/{user_id}/profile/simple", summary="取得簡易的使用者個人資料", response_model=schemas.UserSimple)
def get_user_profile_simple(user_id: int, db: Session = Depends(deps.get_db)):
    """取得簡易版的用戶個人資料"""

    db_user = crud.user.get(db, user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail=f"Can't found user id: {user_id}.")

    return db_user
