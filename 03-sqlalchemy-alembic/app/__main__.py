import uvicorn
from app.core.env_settings import env_settings


def main() -> None:
    """Entrypoint of the application."""

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
    main()
