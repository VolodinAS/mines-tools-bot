import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from app.config import settings
from app.database import init_db


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: Message) -> None:
    """Простая команда для проверки работоспособности бота."""
    if message.chat.id == settings.ADMIN_CHAT_ID:
        await message.answer(
            "✅ Бот запущен и следит за ценами на кристаллы по расписанию (09:00, 15:00, 21:00)."
            )
    else:
        await message.answer("⛔ Доступ запрещён.")


async def main() -> None:
    """Инициализация БД и запуск polling."""
    await init_db()
    logging.info("База данных инициализирована. Запуск бота...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
