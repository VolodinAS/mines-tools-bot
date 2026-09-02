from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_CHAT_ID: int
    MINES_API_TOKEN: str
    DATABASE_URL: str = "sqlite+aiosqlite:////app/data/mines.db"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


settings = Settings()
