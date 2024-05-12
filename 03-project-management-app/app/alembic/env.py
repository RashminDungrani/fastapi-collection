import asyncio

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.env_settings import env_settings
from app.db.base import Base
from app.models import load_all_models

target_metadata = Base.metadata  # type: ignore

load_all_models()


def do_run_migrations(connection):
    # * Don’t Generate Empty Migrations with Autogenerate from (https://alembic.sqlalchemy.org/en/latest/cookbook.html#don-t-generate-any-drop-table-directives-with-autogenerate)
    def process_revision_directives(context, revision, directives):
        if context.config.cmd_opts.autogenerate:  # type: ignore
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []

    context.configure(
        compare_type=True,
        dialect_opts={"paramstyle": "named"},
        connection=connection,
        target_metadata=target_metadata,
        include_schemas=True,
        # literal_binds=True,
        version_table_schema=target_metadata.schema,
        process_revision_directives=process_revision_directives,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_async_engine(env_settings.DB_URL, future=True)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


asyncio.run(run_migrations_online())
