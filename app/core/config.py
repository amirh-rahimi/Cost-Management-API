from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    DATABASE_NAME: str
    SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env"
    )

    @property
    def database_url(self):
        return f"sqlite:///{BASE_DIR / self.DATABASE_NAME}"


settings = Settings()