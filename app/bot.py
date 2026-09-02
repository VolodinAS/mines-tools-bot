import asyncio
import logging
from datetime import datetime, timezone as tz
from zoneinfo import ZoneInfo

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from app.config import CRYSTAL_NAMES, settings
from app.database import get_last_price, init_db, is_price_outdated, save_price
from app.mines_api import mines_api


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
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


@dp.message(Command("get_crystal_price"))
async def cmd_get_crystal_price(message: Message) -> None:
    """Получает актуальные цены на кристаллы (из БД или API)."""
    if message.chat.id != settings.ADMIN_CHAT_ID:
        await message.answer(" Доступ запрещён.")
        return
    
    # Проверяем, нужно ли запрашивать API
    if await is_price_outdated():
        await message.answer("⏳ Данные устарели, запрашиваю API...")
        current_prices = await mines_api.get_crystal_prices()
        await save_price(current_prices)
        last_update_time = datetime.now(tz.utc)
    else:
        current_prices_obj = await get_last_price()
        current_prices = {
            "green": current_prices_obj.green,
            "blue": current_prices_obj.blue,
            "red": current_prices_obj.red,
            "violet": current_prices_obj.violet,
            "white": current_prices_obj.white,
            "cyan": current_prices_obj.cyan,
        }
        last_update_time = current_prices_obj.timestamp
    
    # Форматируем время в читаемый вид (UTC+4 для Самары)
    samara_tz = ZoneInfo("Europe/Samara")
    formatted_time = last_update_time.astimezone(samara_tz).strftime("%d.%m.%Y %H:%M:%S")
    
    # Формируем сообщение с русскими названиями
    report_lines = []
    for color, price in current_prices.items():
        russian_name = CRYSTAL_NAMES.get(color, color.capitalize())
        report_lines.append(f"💎 {russian_name}: {price}")
    
    msg = f"📊 <b>Текущие цены на кристаллы:</b>\n"
    msg += "\n".join(report_lines)
    msg += f"\n\n🕐 <b>Последнее обновление:</b> {formatted_time} (Самара)"
    
    await message.answer(msg, parse_mode="HTML")


async def check_prices_on_startup() -> None:
    """Проверяет цены при запуске бота, если данные устарели."""
    logging.info("Проверка актуальности данных о ценах при запуске...")
    if await is_price_outdated():
        logging.info("Данные устарели, запрашиваю API...")
        current_prices = await mines_api.get_crystal_prices()
        await save_price(current_prices)
        logging.info("Цены успешно обновлены и сохранены в БД.")
    else:
        logging.info("Данные актуальны, запрос к API не требуется.")


async def main() -> None:
    """Инициализация БД, проверка цен и запуск polling."""
    await init_db()
    await check_prices_on_startup()
    logging.info("База данных инициализирована. Запуск бота...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
