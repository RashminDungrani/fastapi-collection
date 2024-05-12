from typing import Optional

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_session import get_db_session
from app.models.user_model import User, UserSecret


class UserDAO:
    """Class for accessing User table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    async def select_one(self, user_id: int) -> User:
        user = await self.session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="user id not found")

        return user

    async def select_from_email(self, email: str) -> User | None:
        query = select(User).where(User.email == email)
        user = (await self.session.execute(query)).scalar_one_or_none()
        return user

    async def select_all(
        self, offset: Optional[int] = None, limit: Optional[int] = None
    ) -> list[User]:
        query = select(User).offset(offset).limit(limit)
        users = (await self.session.execute(query)).scalars().all()
        return users  # type: ignore

    async def insert(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, db_user: User, updated_user: UserSecret) -> User:
        for key, value in updated_user.model_dump(exclude_unset=True).items():
            setattr(db_user, key, value)
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user

    async def hard_delete(self, user_item: User) -> None:
        await self.session.delete(user_item)
        await self.session.commit()
