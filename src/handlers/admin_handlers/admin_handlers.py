import math

from aiogram import Router, types, F
from aiogram.filters import CommandStart, StateFilter, Command, or_f
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from src.core.logger import setup_logging
from src.database.crud.admin_crud_operations.category import category_crud
from src.database.crud.admin_crud_operations.service import service_crud
from src.filters.chat_types import ChatTypeFilter, IsAdmin
from aiogram.utils.i18n import (gettext as _)
from aiogram.utils.i18n import I18n
from src.keyboards.reply_kb import create_kb
from src.keyboards.inline_kb import get_callback_btns, get_pagination_keyboard
from src.database.crud.user_crud_operations.user_operations import add_user, add_language, get_user_by_telegram_id
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
        category_name, category_description = message.text.split(" | ")
        category_name_cleaned, category_description_cleaned = category_name.strip(), category_description.strip()

        print(category_name_cleaned, category_description_cleaned)

        if not await category_crud.exists(session=session, name=category_name):
            await category_crud.create(session=session,
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


@admin_router.message(StateFilter(None), or_f(Command("create_service"), __("Создать услугу")))
async def start_create_service(message: types.Message, session: AsyncSession, state: FSMContext):

    categories = await category_crud.pagination(session=session, limit=10, skip=0)

    if not categories:
        return

    total_categories = await category_crud.get_count(session=session)
    total_pages = math.ceil(total_categories / 10)

    category_list_text = "\n".join([f"ID: {cat.category_id} - {cat.name}" for cat in categories])

    text = (
            _("Список доступных категорий (Страница 1/{total_pages}):\n\n") +
            f"{category_list_text}\n\n" +
            _("Пожалуйста, введите сервис в формате:\n*Название | Описание | Цена | ID категории*")
    )

    await message.answer(
        text.format(total_pages=total_pages),
        reply_markup=get_pagination_keyboard(total_pages=total_pages, current_page=1),
    )

    await state.set_state(AdminState.add_service)


@admin_router.callback_query(StateFilter(AdminState.add_service), F.data.startswith("category_page_"))
async def paginate_categories(callback: types.CallbackQuery, session: AsyncSession):

    page_num = int(callback.data.split("_")[-1])
    offset = (page_num - 1) * 10
    categories = await category_crud.pagination(session=session, limit=10, skip=offset)

    if not categories:
        await callback.answer("Категории не найдены", show_alert=True)
        return

    total_categories = await category_crud.get_count(session=session)
    total_pages = math.ceil(total_categories / 10)

    category_list_text = "\n".join([f"ID: `{cat.category_id}` - {cat.name}" for cat in categories])

    text = (
            _("Список доступных категорий (Страница {page_num}/{total_pages}):\n\n") +
            f"{category_list_text}\n\n" +
            _("Пожалуйста, введите сервис в формате:\nНазвание | Описание | Цена | ID категории")
    )

    await callback.message.edit_text(
        text.format(page_num=page_num, total_pages=total_pages),
        reply_markup=get_pagination_keyboard(total_pages=total_pages, current_page=page_num),
    )
    await callback.answer()


@admin_router.message(StateFilter(AdminState.add_service), F.text)
async def create_service_handler(message: types.Message, session: AsyncSession, state: FSMContext):

    try:

        service_name, service_description, service_price, category_id_str = message.text.split(" | ")

        service_name_cleaned = service_name.strip()
        service_description_cleaned = service_description.strip()
        category_id_cleaned = int(category_id_str.strip())
        service_price_cleaned = int(service_price.strip())


        if not await service_crud.exists(session=session,
                                         name=service_name_cleaned,
                                         category_id=category_id_cleaned):

            await service_crud.create(session=session,
                                      name=service_name_cleaned,
                                      description=service_description_cleaned,
                                      category_id=category_id_cleaned,
                                      price=service_price_cleaned,
                                      creator_id=message.from_user.id)
            await message.answer(_("Услуга создана!"))
            await state.clear()

        else:
            await message.answer(_("Услуга уже создана, придумайте другую!."))

    except ValueError:
        logger.error("Неправильный ввод", message.text)
        await message.answer(_("<b>Ошибка!</b> Пожалуйста, проверьте ввод.\n"
                               "Он должен быть таким:\n"
                               "<code>Название | Описание | Цена | ID категории</code>"))
    except Exception as e:
        logger.error(f"Неизвестная ошибка при создании сервиса: {e}")
        await message.answer(_("Произошла непредвиденная ошибка. Попробуйте снова."))