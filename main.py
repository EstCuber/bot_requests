import asyncio
from aiogram import Bot, Dispatcher, types
import logging

from aiogram.enums import ParseMode

from config import BOT_TOKEN, ADMIN_ID, setup_logging

setup_logging()
logger = logging.getLogger(__name__)


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

async def on_shutdown(bot):
    logger.info("Бот упал")

async def main():
    try:
        logger.info("Бот запущен!")

        dp.shutdown.register(on_shutdown)
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logger.critical(f"Бот не смог запустится! Критическая ошибка:"
                        f"{e}")

if __name__ == '__main__':
    asyncio.run(main())
