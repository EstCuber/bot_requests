import math

from aiogram import Router, types, F
from aiogram.filters import StateFilter, Command, or_f
from aiogram.fsm.context import FSMContext

from aiogram.utils.i18n import (gettext as _)

from sqlalchemy.ext.asyncio import AsyncSession

from src.callback_data.user import PageCallbackData, CategoryPageCallbackData
from src.database.crud.admin_crud_operations.category import category_crud
from src.database.crud.admin_crud_operations.service import service_crud
from src.filters.chat_types import LazyText as __, IsAdmin
from src.handlers.admin_handlers.common.pagination_helper import page_callback
from src.keyboards.inline_kb import get_pagination_keyboard, service_pagination_kb
from src.states.user_state import UserState

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

    await state.set_state(UserState.order_state)

@order_router.callback_query(CategoryPageCallbackData.filter(), ~IsAdmin())
async def page_handler(call: types.CallbackQuery,
                       session: AsyncSession,
                       callback_data: CategoryPageCallbackData) -> None:
    text_template = (
        "Список доступных категорий (Страница {current_page}/{total_pages}):\n\n"
        "{item_list}\n\n"
        "Выберите айди категории!"
    )

    def format_category(item):
        return f"ID: {item.category_id} - {item.name}"

    await page_callback(
        call=call,
        callback_data=callback_data,
        session=session,
        crud_manager=category_crud,
        item_formatter=format_category,
        base_text=text_template
    )
@order_router.message(StateFilter(UserState.order_state), F.text)
async def order_handler(
        message: types.Message,
        state: FSMContext,
        session: AsyncSession
) -> None:
    try:
        category_id = int(message.text.strip())
    except ValueError:
        await message.answer("Вы вели какую-то белиберду! Пожалуйста, введите айди!")
        return


    services = await service_crud.pagination_by_category_id(
        session=session,
        category_id=category_id,
        limit=10,
        skip=0
    )

    if not services:
        await message.answer("Упс! У данной категории нет сервисов, извините! Возвращаем вас к прошлому шагу!")
        return

    total_services = await service_crud.get_services_count_by_category_id(session=session, category_id=category_id)
    total_pages = math.ceil(total_services / 10)

    service_list_text = "\n".join([f"ID: {serv.service_id} - {serv.name}" for serv in services])

    text = (
            _("Список доступных категорий (Страница 1/{total_pages}):\n\n") +
            f"{service_list_text}\n\n" +
            _("Выберите айди сервиса!")
    )

    await message.answer(
        text.format(
            total_pages=total_pages),
            reply_markup=service_pagination_kb(
            total_pages=total_pages,
            category_id=category_id,
            current_page=1),
    )

    await message.answer("потом тут будет выбор сервиса, а пока - простите")


@order_router.message(
    or_f(
        Command("current_order"),
        __("Состояние текущего заказа")
    )
)
async def current_order_handler(message: types.Message) -> None:
    await message.answer("nihao")

