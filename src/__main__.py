import asyncio
from aiogram import Bot, Dispatcher
import logging

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.common.polling import polling
from src.common.bot_commands import setup_bot_commands
from src.filters.chat_types import ChatTypeFilter
from src.handlers.admin_handlers.routers import include_admin_routers
from src.handlers.user_handlers.routers import include_user_routers
from src.core.settings import settings
from src.core.logger import setup_logging

from src.middlewares.registration import register_middlewares

setup_logging()
logger = logging.getLogger(__name__)

async def main(bot_id) -> None:

    bot = Bot(
        token=bot_id,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher()
    dp.message.filter(ChatTypeFilter(['private'])) # фильтруем всего бота на доступ только к личному чату


    # старт самого бота
    register_middlewares(dp)
    include_admin_routers(dp)
    include_user_routers(dp)
    await setup_bot_commands(bot)
    await polling(dp, bot)

if __name__ == '__main__':
    try:
        asyncio.run(main(settings.BOT_TOKEN))
    except Exception as e:
        logger.critical(f"Совершена критическая ошибка при запуске. Ошибка: {e}")