"""
directly insert after creating database
"""

from uuid import uuid4

from fastapi import HTTPException
from pydantic import SecretStr
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.engine import create_async_engine

from app.auth.auth_handler import auth_handler
from app.core.env_settings import env_settings

# from app.core.dependencies import container
from app.models.user_model import User, UserInput


async def insert_initial_data() -> None:
    connectable = create_async_engine(str(env_settings.DB_URL))

    async with connectable.connect() as connection:
        session = AsyncSession(bind=connection)

        # App specific code
        if not env_settings.DB_ADMIN_PASSWORD or not env_settings.DB_ADMIN_EMAIL:
            raise HTTPException(
                status_code=417,
                detail="Expected DB_ADMIN_EMAIL and DB_ADMIN_PASSWORD but it's none",
            )
        try:
            admin = UserInput(
                email=env_settings.DB_ADMIN_EMAIL,
                first_name="Admin",
                last_name="Administrator",
                password=SecretStr(env_settings.DB_ADMIN_PASSWORD),
            )
            assert admin.password
            hashed_password = auth_handler.get_hash_password(
                admin.password.get_secret_value()
            )
            session.add(
                User(
                    **admin.model_dump(exclude={"password"}),
                    **{
                        "id": uuid4(),
                        "hashed_password": hashed_password,
                        "is_admin": True,
                    },
                )
            )
            await session.commit()
            # TODO: LOG with colorized text
            print("Admin added in users table")
        except exc.IntegrityError:
            # Handle the case where the row already exists
            pass

    await connectable.dispose()
