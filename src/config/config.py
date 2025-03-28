from functools import lru_cache
from pydantic import BaseSettings

class Settings(BaseSettings):
    env_name: str = "Local"
    base_url: str = "http://localhost:8000"
    db_url: str = "sqlite:///C:/Users/gslim/URL_Project/src/db/database.db"

    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached instance of the Settings class, which is populated with the appropriate environment values from the .env file.
    
    This function is decorated with lru_cache, so it will only read the .env file once and
    return a cached instance of the Settings class on subsequent calls.
    """
    
    settings = Settings()
    print(f"Loading settings for: {settings.env_name}")
    return settings
