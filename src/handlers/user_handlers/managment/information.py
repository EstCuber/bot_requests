from aiogram import Router, types, F, Bot
from aiogram.filters import CommandStart, StateFilter, Command, or_f
from aiogram.fsm.context import FSMContext

from aiogram.utils.i18n import (gettext as _)
from aiogram.utils.i18n import I18n

from src.core.settings import settings
from src.filters.chat_types import LazyText as __
from src.states.user_state import UserState

info_router = Router()

@info_router.message(
    or_f(
        Command("info"),
        __("Информация")
    )
)
async def info_handler(message: types.Message) -> None:
    await message.answer(_("Здравствуйте, мы такая-то компания, делаем такое то задачи, данный бот просто делает заказики"))

    #TODO: может продумать тоже несколько инлайн или реплай кнопок, но в таком случае также добавить main_kb
    #TODO: вообще, попробовать бы сделать main_kb как-то отдельно где-то. Или каждый раз отправлять одну и ту же кб
    #Основная проблема данной реализации в том, что придется дублировать очень много кода, что является не очень хорошей практикой

    # Решение:
    #Попробовать продумать создание клавиатуры (провести тесты насчет выбранного языка юзером. Возможно просто константно создавать кб ПОСЛЕ выбора языка уже пользователем)

