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
    
    # Path constants for "Self-Healing" logic (Annotated for Pydantic)
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
    LOGS_DIR: str = "logs"
    STORAGE_DIR: str = "storage"
    TEMP_AUDIO_DIR: str = "storage/temp_audio"

    def ensure_directories(self):
        required_folders = [self.LOGS_DIR, self.STORAGE_DIR, self.TEMP_AUDIO_DIR]
        
        for folder in required_folders:
            # os.makedirs creates the folder for you.
            # "exist_ok=True" means it ignores the command if the folder already exists (Self-Healing!)
            os.makedirs(folder, exist_ok=True)

# Instantiate a global config object to be imported elsewhere
config = Settings()

# Run our self-healing check as soon as config is loaded (when the bot starts)
config.ensure_directories()
