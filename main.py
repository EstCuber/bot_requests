import asyncio
from aiogram import Bot, Dispatcher, types
import logging

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.i18n import FSMI18nMiddleware

from crud.engine import session_maker
from handlers.user_handlers import user_router
from config import settings, setup_logging
from locales.engine import i18n
from middlewares.db_session import DataBaseSession
from middlewares.language_middleware import LanguageMiddleware

setup_logging()
logger = logging.getLogger(__name__)


async def on_startup(bot) -> None:
    logger.info("Бот запущен и готов к работе!")


async def on_shutdown(bot) -> None:
    logger.info("Бот остановлен")

async def main() -> None:

    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher()
    dp.include_routers(
        user_router
    )

    dp.update.middleware.register(DataBaseSession(session_pool=session_maker))
    dp.update.middleware.register(LanguageMiddleware(session_pool=session_maker))
    dp.update.middleware.register(FSMI18nMiddleware(i18n))

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    logger.info("Бот в процессе запуска...")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        logger.critical(f"Совершена критическая ошибка при запуске. Ошибка: {e}")