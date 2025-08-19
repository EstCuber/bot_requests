from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.database.user_operations import get_user_by_telegram_id

class LanguageMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        session = data["session"]

        user = getattr(event, "from_user", None)
        if user:

            db_user = await get_user_by_telegram_id(session, user.id)
            if db_user and db_user.language:
                data["locale"] = db_user.language

        return await handler(event, data)