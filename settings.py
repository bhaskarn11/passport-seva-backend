from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "Passport Seva API"
    version: str = "v1"
    app_description: str = "Passport Seva Backend API"
    model_config = SettingsConfigDict(env_file=".env", extra="allow")


@lru_cache()
def get_settings():
    settings = Settings()
    print("Loading settings...")
    return settings
