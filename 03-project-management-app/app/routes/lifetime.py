from asyncio import current_task
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from app.core.env_settings import env_settings


def _setup_db(app: FastAPI) -> None:  # pragma: no cover
    """
    Creates connection to the database.

    This function creates SQLAlchemy engine instance,
    session_factory for creating sessions
    and stores them in the application's state property.

    :param app: fastAPI application.
    """
    engine = create_async_engine(str(env_settings.DB_URL), echo=env_settings.DB_ECHO)
    session_factory = async_scoped_session(
        sessionmaker(
            engine,  # type: ignore
            expire_on_commit=False,
            class_=AsyncSession,  # type: ignore
        ),
        scopefunc=current_task,
    )
    app.state.db_engine = engine
    app.state.db_session_factory = session_factory


@asynccontextmanager
async def lifespan(app: FastAPI):
    _setup_db(app)
    # print('db connected')
    yield
    await app.state.db_engine.dispose()
    # print("db connections close.")
