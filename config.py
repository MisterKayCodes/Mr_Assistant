import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings using pydantic-settings.
    This reads from environment variables or a .env file automatically.
    """
    bot_token: str
    database_url: str = "sqlite+aiosqlite:///storage/app.sqlite"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    def ensure_directories(self):
        # List of required folders (e.g. for logs or audio files we might store later)
        # We need "logs" for errors.log, "storage" for the database, and "storage/temp_audio" for Voice messages
        required_folders = ["logs", "storage", "storage/temp_audio"]
        
        for folder in required_folders:
            # os.makedirs creates the folder for you.
            # "exist_ok=True" means it ignores the command if the folder already exists (Self-Healing!)
            os.makedirs(folder, exist_ok=True)

# Instantiate a global config object to be imported elsewhere
config = Settings()

# Run our self-healing check as soon as config is loaded (when the bot starts)
config.ensure_directories()
