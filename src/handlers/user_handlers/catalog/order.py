from aiogram import Router, types, F, Bot
from aiogram.filters import CommandStart, StateFilter, Command, or_f
from aiogram.fsm.context import FSMContext

from aiogram.utils.i18n import (gettext as _)
from aiogram.utils.i18n import I18n

from src.core.settings import settings
from src.filters.chat_types import LazyText as __
from src.states.user_state import UserState

order_router = Router()

@order_router.message(or_f(Command("order"), __("Заказ")))
async def start_order(message: types.Message, state: FSMContext) -> None:
    await message.answer("Чтобы заказать, вам необходимо выбрать из предложенных вариантов категории")

    # здесь будут кнопки на пагинации,
    # т.е, будет 10 возможных кнопок, две из которых - вперед и назад.

@order_router.message(or_f(Command("current_order"), __("Состояние текущего заказа")))
async def current_order_handler(message: types.Message) -> None:
    await message.answer("Здесь будет состояние текущего заказа")

