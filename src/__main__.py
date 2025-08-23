import asyncio
from aiogram import Bot, Dispatcher
import logging

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.common.polling import polling
from src.common.bot_commands import set_and_delete_commands
from src.handlers.admin_handlers.admin_handlers import admin_router
from src.handlers.user_handlers import user_router
from src.core.settings import settings
from src.core.logger import setup_logging

from src.middlewares.registration import registration_middlewares

setup_logging()
logger = logging.getLogger(__name__)

async def main() -> None:

    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher()
    dp.include_routers(
        admin_router,
        user_router
    )

    registration_middlewares(dp)
    await set_and_delete_commands(bot)
    await polling(dp, bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        logger.critical(f"Совершена критическая ошибка при запуске. Ошибка: {e}")