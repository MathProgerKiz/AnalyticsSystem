from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./analytics.db"
    debug: bool = True

    #GIGACHAT CONFIG
    AUTH_KEY_GIGACHAT: str

    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug(cls, value):
        if isinstance(value, str) and value.lower() in {"release", "prod", "production"}:
            return False
        return value

    class Config:
        env_file = ".env"


settings = Settings()
