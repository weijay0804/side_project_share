"""

    使用者認證相關路由

"""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import create_jwt_token
from app.schemas import JwtToken
from app.api.deps import get_db
from app.core import config
from app import crud

router = APIRouter()


@router.post("/token", response_model=JwtToken, summary="使用者登入並回傳 jwt token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """使用者登入並獲得 jwt token"""

    # NOTE 這邊的 username 是因為 `OAuth2PasswordRequestForm` 的格式定義的，實際上是要傳入 email
    # 所以在前端的 form 中需要寫成這樣的格式
    # {"username" : "test@test.com", "password" : "user_password"}
    user = crud.user.authenticate(db, email=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expire = timedelta(minutes=config.settings.JWT_TOKEN_EXP_MIN)
    access_token = create_jwt_token(
        data={"sub": user.email},
        key=config.settings.JWT_SRCRET_KEY,
        expire_delta=access_token_expire,
        algorithm=config.settings.JWT_ALGORITHM,
    )

    return {"access_token": access_token, "token_type": "bearer"}
