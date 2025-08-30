import asyncio
import math

from aiogram import Router, types, F
import logging

from src.callback_data.user import CategoryPageCallbackData
from src.core.logger import setup_logging
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.utils.i18n import I18n, gettext as _
from src.filters.chat_types import LazyText as __

from src.database.crud.admin_crud_operations.category import category_crud
from src.handlers.admin_handlers.common.pagination_helper import page_callback
from src.keyboards.inline_kb import get_pagination_keyboard, get_callback_btns
from src.states.admin_state import AdminState

setup_logging()
logger = logging.getLogger(__name__)

admin_category_router = Router()


@admin_category_router.message(
    StateFilter(None),
    or_f(Command("create_category"),
         __("Создать категорию")))
async def before_create_category(
        message: types.Message,
        state: FSMContext):

    await message.answer(_("Пожалуйста, введите категорию в формате:\n"
                   "Название категории | Описание категории"), reply_markup=get_callback_btns(btns={_("отмена"): "_cancel"}))
    await state.set_state(AdminState.add_category)

@admin_category_router.callback_query(
    StateFilter(AdminState.add_category),
    F.data.startswith("_cancel")
)
async def cancel_category_creation(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer(_("Произошла отмена создания категории!"))
    await state.clear()

    await asyncio.sleep(1.5)
    await callback.message.delete()

@admin_category_router.message(
    StateFilter(AdminState.add_category),
    F.text)
async def create_category(
        message: types.Message,
        session: AsyncSession,
        state: FSMContext):

    try:
        (category_name,
         category_description) = message.text.split(" | ")

        (category_name_cleaned,
         category_description_cleaned) = category_name.strip(), category_description.strip()

        if not await category_crud.exists(
                session=session,
                name=category_name):

            await category_crud.create(
                session=session,
                name=category_name_cleaned,
                description=category_description_cleaned,
                creator_id=message.from_user.id)

            await message.answer(_("Ваша категория создана, поздравляю!"))
            await state.clear()

        else:
            await message.answer(_("Данная категория уже существует! Введите еще раз!"))

    except ValueError:
        logger.error("Пользователь ввел неправильные данные!")
        await message.answer(_("Вы неправильно указали название и описание"))

    except Exception as e:
        await message.answer(_("Попробуйте еще раз ввести название и описание!"))
        logger.error(f"Ошибка введения описания: {e}")


