from typing import Optional
from datetime import timedelta, datetime

from jose import jwt
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_jwt_token(
    data: dict,
    *,
    key: str,
    algorithm: Optional[str] = "HS256",
    expire_delta: Optional[timedelta] = None
) -> str:
    """產生 JWT Token

    Args:
        data: 要放在 token 中的資料
        key: secret key
        algorithm: 加密的演算法種類. Defaults to `"HS256"`.
        expire_delta: token 過期時間 (默認為 15 分鐘). Defaults to None.
    """

    to_encode = data.copy()

    if expire_delta:
        expire = datetime.utcnow() + expire_delta

    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, key, algorithm=algorithm)

    return encoded_jwt
