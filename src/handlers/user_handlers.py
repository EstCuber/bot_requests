from aiogram import Router, types, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.filters.chat_types import ChatTypeFilter
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import I18n
from src.keyboards.user_kb import create_kb
from src.keyboards.inline_kb import get_callback_btns
from src.database.user_operations import add_user, add_language, get_user_by_telegram_id

user_router = Router()
user_router.message.filter(ChatTypeFilter(['private']))

@user_router.message(CommandStart())
async def cmd_start(message: types.Message, session: AsyncSession) -> None:
    user = await get_user_by_telegram_id(session=session, telegram_id=int(message.from_user.id))

    if getattr(user, "language", None) is None:

        await message.answer("Please, choose your language",
                             reply_markup=get_callback_btns(btns={"ru": "_ru",
                                                            "eng": "_en"}))
        await add_user(
            session=session,
            telegram_id=int(message.from_user.id),
            username=message.from_user.username,
        )

    else:
        text = _("Добро пожаловать снова! Рады Вам снова служить!", locale=user.language)
        await message.answer(text=text, reply_markup=create_kb(
        _("Информация", locale=user.language),
        _("Состояние текущего заказа", locale=user.language),
        _("Поддержка", locale=user.language),
        sizes=(2, 1)
    ))
@user_router.callback_query(StateFilter(None), F.data.startswith("_"))
async def choose_lang(callback: types.CallbackQuery, state: FSMContext, i18n: I18n, session: AsyncSession) -> None:
    lang = callback.data.split("_")[-1]
    await state.update_data(locale=lang)

    await add_language(session=session,
                       telegram_id=callback.from_user.id,
                       lang=lang)

    text = i18n.gettext(""
"Добро пожаловать, пользователь! Рад приветствовать тебя в нашем боте:\n"
"    В этом боте вы можете оставить свой заказ, который мы обязательно "
"выполним. Со спектром наших услуг вы можете ознакомиться\n"
"    по команде /info, но перед этим вам нужно внести некоторые данные", locale=lang)

    main_user_kb = create_kb(
        i18n.gettext("Информация", locale=lang),
        i18n.gettext("Состояние текущего заказа", locale=lang),
        i18n.gettext("Поддержка", locale=lang),
        sizes=(2, 1)
    )

    await callback.message.delete()
    await callback.message.answer(text, reply_markup=main_user_kb)

#TODO: сделать работу с кнопками, проработать момент того что какая кнопка делает, понять работает ли перевод