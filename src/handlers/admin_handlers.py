from aiogram import Router, types, F
from aiogram.filters import CommandStart, StateFilter, Command, or_f
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from src.core.logger import setup_logging
from src.database.admin_operations import orm_create_category, check_category_exists
from src.filters.chat_types import ChatTypeFilter, IsAdmin
from aiogram.utils.i18n import (gettext as _)
from aiogram.utils.i18n import I18n
from src.keyboards.reply_kb import create_kb
from src.keyboards.inline_kb import get_callback_btns
from src.database.user_operations import add_user, add_language, get_user_by_telegram_id
from src.filters.chat_types import LazyText as __
from src.states.admin_state import AdminState

setup_logging()
logger = logging.getLogger(__name__)

admin_router = Router()
admin_router.message.filter(IsAdmin(), ChatTypeFilter(['private']))

@admin_router.message(CommandStart())
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
@admin_router.callback_query(StateFilter(None), F.data.startswith("_"))
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


@admin_router.message(StateFilter(None), or_f(Command("create_category"), __("Создать категорию")))
async def create_category(message: types.Message, state: FSMContext):
    await message.answer(_("Пожалуйста, введите категорию в формате:\n"
                   "Название категории | Описание категории"))

    await state.set_state(AdminState.add_category)

@admin_router.message(StateFilter(AdminState.add_category), F.text)
async def create_category_handler(message: types.Message, session: AsyncSession, state: FSMContext):

    try:
        name, description = message.text.split(" | ")
        name, description = name.strip(), description.strip()
        await state.update_data(name=name, description=description)

        data = await state.get_data()

        if not await check_category_exists(session=session, category_name=name):
            await orm_create_category(session=session, data=data)
            await message.answer(_("Ваша категория создана, поздравляю!"))
            await state.clear()
        else:
            await message.answer(_("Данная категория уже существует! Введите еще раз!"))

    except ValueError:
        logger.error("Пользователь ввел неправильные данные!")
        await message.answer(_("Вы неправильно указали название и описание"))
    except Exception as e:
        await message.answer(_("Попробуйте еще раз ввести название и описание!"))

