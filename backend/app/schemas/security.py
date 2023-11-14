from typing import Optional
from pydantic import BaseModel


class JwtToken(BaseModel):
    access_token: str
    token_type: str


class JwtTokenData(BaseModel):
    email: Optional[str] = None
