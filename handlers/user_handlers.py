from aiogram import Router, types, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from filters.chat_types import ChatTypeFilter
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import I18n
from keyboards.user_kb import create_kb
from keyboards.inline_kb import get_callback_btns
user_router = Router()
user_router.message.filter(ChatTypeFilter(['private']))

@user_router.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    await message.answer("Please, choose your language",
                         reply_markup=get_callback_btns(btns={"ru": "_ru",
                                                        "eng": "_en"}))
    #TODO: Подключить базы данных, здесь написать логику с машиной состояния и собирание нужной информации о клиенте

@user_router.callback_query(StateFilter(None), F.data.startswith("_"))
async def choose_lang(callback: types.CallbackQuery, state: FSMContext, i18n: I18n) -> None:
    lang = callback.data.split("_")[-1]
    await state.update_data(locale=lang)

    text = i18n.gettext(""
"Добро пожаловать, пользователь! Рад приветствовать тебя в нашем боте:\n"
"    В этом боте вы можете оставить свой заказ, который мы обязательно "
"выполним. Со спектром наших услуг вы можете ознакомиться\n"
"    по команде /info, но перед этим вам нужно внести некоторые данные", locale=lang)

    main_user_kb = create_kb(
        _("Информация"),
        _("Состояние текущего заказа"),
        _("Поддержка"),
        sizes=(2, 1)
    )

    #TODO: отправляем data в бд - инфа о пользователе
    await callback.message.delete()
    await callback.message.answer(text, reply_markup=main_user_kb)