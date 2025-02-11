from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="./config/.env", env_file_encoding="utf-8")

    APP_TITLE: str = "FastAPI"
    VERSION: str = "1.0.0"
    PORT: int = 8000

    DATABASE_URL: str = "sqlite+aiosqlite:///./database.db"
    CHECK_SAME_THREAD: bool = False

    CORS_ORIGINS: list[str] = ["*"]
    DEBUG: bool = False

    LOG_LEVEL: str = "INFO"


settings = Settings()
