from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserResponse(BaseModel):
    username: str
    disabled: bool
    access_token: Optional[str] = None
    token_expires_at: Optional[datetime] = None


class User(UserResponse):
    password: str
    hashed_password: Optional[str] = None
