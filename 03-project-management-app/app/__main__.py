import asyncio

import uvicorn

from app.core.env_settings import env_settings
from app.db.insert_initial_data import insert_initial_data


async def main() -> None:
    """Entrypoint of the application."""
    await insert_initial_data()

    uvicorn.run(
        "app.routes.application:get_app",
        workers=env_settings.SERVER_WORKERS,
        host=env_settings.SERVER_HOST,
        port=env_settings.SERVER_PORT,
        reload=env_settings.SERVER_RELOAD,
        factory=True,
        ssl_certfile=env_settings.SSL_FULL_CHAIN_PATH,
        ssl_keyfile=env_settings.SSL_PRIVATE_KEY_PATH,
    )


if __name__ == "__main__":
    asyncio.run(main())
