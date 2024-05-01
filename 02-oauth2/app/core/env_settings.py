import enum
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

# TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class ENVSettings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    model_config = SettingsConfigDict(
        env_file="envs/.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    ENV_NAME: str

    ## FastAPI envs
    APP_NAME: str = ""
    APP_DESC: str = ""
    APP_VERSION: str = "0.1.0"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    ## server  settings
    SERVER_WORKERS: int = 1
    SERVER_RELOAD: bool = False

    ## logging settings
    LOG_LEVEL: LogLevel = LogLevel.INFO

    ## Auth settings
    JWT_SECRET: str = ""  # openssl rand -hex 32
    JWT_ALG: str = "HS256"
    JWT_EXP: int = 5  # minutes
    # REFRESH_TOKEN_EXP_IN_MIN: int = 60 * 24 * 365 * 100  # 100 years
    # ACCESS_TOKEN_EXP_IN_MIN: int = 60 * 24 * 365 * 10  # 10 year

    # ssl file paths
    SSL_FULL_CHAIN_PATH: Optional[str] = None
    SSL_PRIVATE_KEY_PATH: Optional[str] = None


@lru_cache
def get_env_settings(env_file_path: str = "envs/.env") -> ENVSettings:
    env_settings = ENVSettings(_env_file=env_file_path, _env_file_encoding="utf-8")  # type: ignore
    print(f">> {env_settings.ENV_NAME=}")
    return env_settings


env_settings = get_env_settings(
    # "envs/.env",
    # "envs/dev.env",
    # "envs/prod.env",
    # "envs/prod_test.env",
)
