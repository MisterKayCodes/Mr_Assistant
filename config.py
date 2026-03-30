import os
from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# THE DYNAMIC PULSE: Loading .env BEFORE settings are initialized.
# This ensures that every process restart pulls fresh data from the disk.
load_dotenv(find_dotenv(), override=True)

class Settings(BaseSettings):
    """
    Configuration Layer: The single source of truth for the organism.
    Rule 11: Separation of Concerns.
    """
    bot_token: str
    database_url: str = "sqlite+aiosqlite:///storage/app.sqlite"
    openai_api_key: str = ""

    # Pydantic Settings will look for these in the environment
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

config = Settings()
