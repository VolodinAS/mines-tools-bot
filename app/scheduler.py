from zoneinfo import ZoneInfo

from aiocron import crontab

from app.bot import bot, settings
from app.database import get_last_price, save_price
from app.mines_api import mines_api


# Расписание: 0 минут, 9, 15 и 21 час. Часовой пояс: Самара (UTC+4).
@crontab("0 9,15,21 * * *", tz=ZoneInfo("Europe/Samara"))
async def check_prices_task() -> None:
    """Основная задача: проверяет цены, сравнивает с прошлыми и шлёт алерт."""
    current_prices = await mines_api.get_crystal_prices()
    last_price = await get_last_price()
    
    increased_crystals = []
    report_lines = []
    
    for color, price in current_prices.items():
        color_cap = color.capitalize()
        if last_price:
            last_val = getattr(last_price, color, 0)
            if price > last_val:
                increased_crystals.append(f"🔺 <b>{color_cap}</b>: {last_val} ➡️ <b>{price}</b>")
        
        report_lines.append(f"💎 {color_cap}: {price}")
    
    # Формируем сообщение (используем \n для корректных переносов)
    if increased_crystals:
        msg = "⚠️ <b>Внимание! Цены на кристаллы повысились:</b>\n\n"
        msg += "\n".join(increased_crystals)
        msg += "\n\n📊 <b>Полный прайс на текущий момент:</b>\n" + "\n".join(report_lines)
    else:
        msg = "📊 <b>Текущие цены на кристаллы:</b>\n" + "\n".join(report_lines)
    
    await bot.send_message(settings.ADMIN_CHAT_ID, msg, parse_mode="HTML")
    
    await save_price(current_prices)
