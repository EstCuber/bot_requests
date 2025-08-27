import math

from aiogram import Router, types, F
from aiogram.filters import StateFilter, Command, or_f
from aiogram.fsm.context import FSMContext

from aiogram.utils.i18n import (gettext as _)

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.crud.admin_crud_operations.category import category_crud
from src.filters.chat_types import LazyText as __
from src.keyboards.inline_kb import get_pagination_keyboard


order_router = Router()

@order_router.message(
    or_f(
        Command("order"),
        __("Заказ")
    )
)
async def start_order(
        message: types.Message,
        state: FSMContext,
        session: AsyncSession
) -> None:

    await message.answer("Чтобы заказать, вам необходимо выбрать из предложенных вариантов категории")

    categories = await category_crud.pagination(
        session=session,
        limit=10,
        skip=0)

    total_categories = await category_crud.get_count(session=session)
    total_pages = math.ceil(total_categories / 10)

    category_list_text = "\n".join([f"ID: {cat.category_id} - {cat.name}" for cat in categories])

    text = (
            _("Список доступных категорий (Страница 1/{total_pages}):\n\n") +
            f"{category_list_text}\n\n" +
            _("Выберите айди категории!")
    )

    await message.answer(
        text.format(
            total_pages=total_pages),
        reply_markup=get_pagination_keyboard(
            total_pages=total_pages,
            current_page=1),
    )
    #TODO: дореализовать функцию до конца!

@order_router.message(
    or_f(
        Command("current_order"),
        __("Состояние текущего заказа")
    )
)
async def current_order_handler(message: types.Message) -> None:
    await message.answer("Здесь будет состояние текущего заказа")

