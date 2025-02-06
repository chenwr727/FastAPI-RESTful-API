from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_TITLE: str = "FastAPI"
    VERSION: str = "1.0.0"
    PORT: int = 8000

    DATABASE_URL: str = "sqlite:///database.db"
    CHECK_SAME_THREAD: bool = False
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = "../config/.env"
        env_file_encoding = "utf-8"


settings = Settings()
