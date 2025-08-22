
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.database.crud.user_crud_operations.user_operations import get_user_by_telegram_id


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
        state: FSMContext = data["state"]
        user = data["event_from_user"]

        if user:

            db_user = await get_user_by_telegram_id(session, user.id)
            if db_user and db_user.language:
                data["locale"] = db_user.language

                if state:
                    await state.update_data(locale=db_user.language)

        return await handler(event, data)