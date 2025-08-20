import logging
from src.core.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

async def polling(dp, bot):
    on_start(dp)
    logger.info("Бот в процессе запуска...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

async def on_startup(bot) -> None:
    logger.info("Бот запущен и готов к работе!")


async def on_shutdown(bot) -> None:
    logger.info("Бот остановлен")

def on_start(dp):
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)