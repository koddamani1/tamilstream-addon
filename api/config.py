import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "TamilStream"
    app_version: str = "1.0.0"
    app_description: str = "Tamil Movies & Series Stremio Addon with TorBox Integration"
    
    mongodb_uri: str = os.getenv("MONGODB_URI", "")
    database_name: str = "tamilstream"
    
    torbox_api_url: str = "https://api.torbox.app/v1"
    
    secret_key: str = os.getenv("SESSION_SECRET", "tamilstream-secret-key")
    
    scraper_interval_hours: int = 6
    
    cache_ttl: int = 3600
    
    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
