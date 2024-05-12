"""
User Model
"""

import datetime

from pydantic import UUID4, BaseModel, EmailStr, Field, SecretStr
from sqlalchemy import (
    UUID,
    Boolean,
    DateTime,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class User(Base):
    __tablename__: str = "User"

    id: Mapped[UUID4] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
    )
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(
        String,
        index=True,
        unique=True,
        nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column(String(256), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_disabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    modified_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )
    deleted_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True),
        default=None,
        nullable=True,
    )


## Pydantic models
class UserSecret(BaseModel):
    password: SecretStr | None = Field(
        default=None, min_length=6, max_length=256, exclude=True
    )


class UserInput(UserSecret):
    email: EmailStr = Field()
    first_name: str = Field(min_length=1, max_length=256)
    last_name: str = Field(min_length=1, max_length=256)
    is_verified: bool | None = False


class UserResponse(UserInput):
    id: UUID4
    created_at: datetime.datetime = Field()
    modified_at: datetime.datetime | None = None


class LoginResponseModel(BaseModel):
    access_token: str  # This is important key (access_key) for OAuth2 and swagger to see get token
    token_type: str
    token_issued_at: datetime.datetime | None = None
    token_expires_at: datetime.datetime | None = None
    user: UserResponse

    # model_config = ConfigDict(from_attributes=True)
