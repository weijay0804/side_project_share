from typing import Generator

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer


from app import crud
from app.db.session import SessionLocal
from app.schemas.security import JwtTokenData
from app.models import User
from app.core import config


# NOTE 定義 JWT 認證格式
# 其中的 `token` 是認證 api 的路徑（相對路徑）
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db

    finally:
        db.close()


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    """根據 JWT token 取得使用者"""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not valudate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, config.settings.JWT_SRCRET_KEY, algorithms=config.settings.JWT_ALGORITHM
        )
        email = payload.get("sub")

        if email is None:
            raise credentials_exception

        token_data = JwtTokenData(email=email)

    except JWTError:
        raise credentials_exception

    user = crud.user.get_by_email(db, email=token_data.email)

    if user is None:
        raise credentials_exception

    return user
