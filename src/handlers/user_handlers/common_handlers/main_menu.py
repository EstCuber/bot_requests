from aiogram import Router, types, F
from aiogram.filters import CommandStart, StateFilter, Command, or_f
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.filters.chat_types import ChatTypeFilter
from aiogram.utils.i18n import (gettext as _)
from aiogram.utils.i18n import I18n
from src.keyboards.reply_kb import create_kb
from src.keyboards.inline_kb import get_callback_btns
from src.database.crud.user_crud_operations.user_operations import add_user, add_language, get_user_by_telegram_id
from src.filters.chat_types import LazyText as __


main_menu_router = Router()


@main_menu_router.message(or_f(Command("info"), __("Информация")))
async def info_handler(message: types.Message) -> None:
    await message.answer("Здесь будет информация")

@main_menu_router.message(or_f(Command("current_order"), __("Состояние текущего заказа")))
async def current_order_handler(message: types.Message) -> None:
    await message.answer("Здесь будет состояние текущего заказа")

@main_menu_router.message(or_f(Command("help"), __("Поддержка")))
async def help_handler(message: types.Message) -> None:
    await message.answer("Здесь будет поддержка")