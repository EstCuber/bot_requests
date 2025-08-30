import math
from typing import Callable, Any

from aiogram import types
from sqlalchemy.ext.asyncio import AsyncSession

from src.callback_data.user import PageCallbackData
from src.database.crud.base import CRUDBaseTasks
from src.keyboards.inline_kb import get_pagination_keyboard


async def page_callback(
        call: types.CallbackQuery,
        callback_data: PageCallbackData,
        session: AsyncSession,
        crud_manager: CRUDBaseTasks,
        item_formatter: Callable[[Any], str],
        base_text: str
):
    current_page = callback_data.current_page
    limit = 10
    skip = (current_page - 1) * limit

    items = await crud_manager.pagination(session=session, limit=limit, skip=skip)
    total_categories = await crud_manager.get_count(session=session)
    total_pages = math.ceil(total_categories / limit)

    item_list_text = "\n".join([item_formatter(item) for item in items])

    text = base_text.format(
        item_list=item_list_text,
        current_page=current_page,
        total_pages=total_pages
    )

    await call.message.edit_text(
        text=text,
        reply_markup=get_pagination_keyboard(
            total_pages=total_pages,
            current_page=current_page),
    )
    await call.answer()
