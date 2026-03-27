from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings using pydantic-settings.
    This reads from environment variables or a .env file automatically.
    """
    bot_token: str
    database_url: str = "sqlite+aiosqlite:///app.sqlite"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Instantiate a global config object to be imported elsewhere
config = Settings()
