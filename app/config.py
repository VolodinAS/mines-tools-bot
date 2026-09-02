from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# Маппинг английских названий кристаллов на русские
CRYSTAL_NAMES = {
    "green": "Зеленый",
    "blue": "Синий",
    "red": "Красный",
    "violet": "Фиолетовый",
    "white": "Белый",
    "cyan": "Голубой",
}


class Settings(BaseSettings):
    DEBUG: bool = True
    BOT_TOKEN: str
    ADMIN_CHAT_ID: int
    MINES_API_TOKEN: str
    DATABASE_URL: str = "sqlite+aiosqlite:////app/data/mines.db"
    API_VERIFY_SSL: bool = True  # <-- ДОБАВЛЕНО: явное объявление переменной
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )
    
    @property
    def database_url(self) -> str:
        """Возвращает URL БД: локальный для DEBUG, из .env для продакшена."""
        if not self.DEBUG:
            return self.DATABASE_URL
        data_dir = Path(__file__).parent.parent / "data"
        data_dir.mkdir(exist_ok=True)
        return f"sqlite+aiosqlite:///{data_dir / 'mines.db'}"


settings = Settings()
