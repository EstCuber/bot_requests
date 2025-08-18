from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from filters.chat_types import ChatTypeFilter
from aiogram.utils.i18n import gettext as _
from keyboards.user_kb import create_kb

user_router = Router()
user_router.message.filter(ChatTypeFilter(['private']))

@user_router.message(CommandStart())
async def cmd_start(message: types.Message) -> None:

    main_user_kb = create_kb(
        _("Информация"),
        _("Состояние текущего заказа"),
        _("Поддержка"),
        sizes=(2, 1)
    )

    await message.answer(_("""Добро пожаловать, пользователь! Рад приветствовать тебя в нашем боте:
    В этом боте вы можете оставить свой заказ, который мы обязательно выполним. Со спектром наших услуг вы можете ознакомиться
    по команде /info, но перед этим вам нужно внести некоторые данные"""), reply_markup=main_user_kb)

    #TODO: Подключить базы данных, здесь написать логику с машиной состояния и собирание нужной информации о клиенте
