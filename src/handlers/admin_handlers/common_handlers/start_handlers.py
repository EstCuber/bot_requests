from aiogram import Router, types, F
import logging

from src.core.logger import setup_logging
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.utils.i18n import I18n, gettext as _

from src.database.crud.user_crud_operations.user_operations import get_user_by_telegram_id, add_language, add_user
from src.keyboards.inline_kb import get_callback_btns
from src.keyboards.reply_kb import create_kb

setup_logging()
logger = logging.getLogger(__name__)
admin_start_router = Router()

@admin_start_router.message(CommandStart())
async def admin_cmd_start(message: types.Message, session: AsyncSession) -> None:
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
        text = _("Админ вернулся, ура-ура!", locale=user.language)
        await message.answer(text=text, reply_markup=create_kb(
        _("Создать категорию", locale=user.language),
        _("Создать услугу", locale=user.language),
        _("Поддержка", locale=user.language),
        sizes=(2, 1)
    ))
@admin_start_router.callback_query(StateFilter(None), F.data.startswith("_"))
async def choose_lang(callback: types.CallbackQuery, state: FSMContext, i18n: I18n, session: AsyncSession) -> None:
    lang = callback.data.split("_")[-1]
    await state.update_data(locale=lang)

    await add_language(session=session,
                       telegram_id=callback.from_user.id,
                       lang=lang)

    text = i18n.gettext("Добро пожаловать админ, готов к работе!", locale=lang)

    main_user_kb = create_kb(
        i18n.gettext("Создать категорию", locale=lang),
        i18n.gettext("Создать услугу", locale=lang),
        i18n.gettext("Поддержка", locale=lang),
        sizes=(2, 1)
    )

    await callback.message.delete()
    await callback.message.answer(text, reply_markup=main_user_kb)