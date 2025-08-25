from aiogram import Router, types, F, Bot
from aiogram.filters import CommandStart, StateFilter, Command, or_f
from aiogram.fsm.context import FSMContext

from aiogram.utils.i18n import (gettext as _)
from aiogram.utils.i18n import I18n

from src.core.settings import settings
from src.filters.chat_types import LazyText as __
from src.states.user_state import UserState

main_menu_router = Router()


@main_menu_router.message(or_f(Command("info"), __("Информация")))
async def info_handler(message: types.Message) -> None:
    await message.answer("Здесь будет информация")

@main_menu_router.message(or_f(Command("current_order"), __("Состояние текущего заказа")))
async def current_order_handler(message: types.Message) -> None:
    await message.answer("Здесь будет состояние текущего заказа")

@main_menu_router.message(
    StateFilter(None),
    or_f(Command("help"),
     __("Поддержка")))
async def help_handler(
        message: types.Message,
        state: FSMContext) -> None:

    await message.answer(_("Если у вас появились вопросы, то пожалуйста, задайте свой вопрос! "
                           "Этот бот перешлет ваш вопрос админу!"))
    await state.set_state(UserState.question_state)

@main_menu_router.message(
    StateFilter(UserState.question_state),
    F.text)
async def send_question_from_user(
        message: types.Message,
        state: FSMContext,
        bot: Bot
) -> None:

    await bot.forward_message(
        chat_id=settings.ADMIN_ID, # TODO: переделать после под отправку всем админам? Или одному админу - подумать кароче
        from_chat_id=message.chat.id,
        message_id=message.message_id
    )

    await message.answer(_("Спасибо за ваш вопрос! Скоро администратор с Вами свяжется!"))
    await state.clear()