from typing import Awaitable, Callable, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.database.crud.user_crud_operations.user_operations import get_user_by_telegram_id


class DataBaseSession(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        self.session_pool = session_pool


    async def __call__(self,
                       handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: dict[str, Any]
                       ) -> Any:
        async with self.session_pool() as session:
            data["session"] = session
            from_user = None
            if event.message:
                from_user = event.message.from_user
            elif event.callback_query:
                from_user = event.callback_query.from_user
            elif event.inline_query:
                from_user = event.inline_query.from_user
            elif event.chosen_inline_result:
                from_user = event.chosen_inline_result.from_user
            elif event.shipping_query:
                from_user = event.shipping_query.from_user
            elif event.pre_checkout_query:
                from_user = event.pre_checkout_query.from_user
            if from_user:
                user = await get_user_by_telegram_id(session, telegram_id=from_user.id)
                data["db_user"] = user
            else:
                data["db_user"] = None
            return await handler(event, data)
    # TODO: разобраться в подходе с разделением чтения и записи, поменять все на конструкцию async with