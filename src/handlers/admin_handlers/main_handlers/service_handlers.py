import math

from aiogram import Router, types, F
import logging
from src.core.logger import setup_logging
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.utils.i18n import I18n, gettext as _

from src.database.crud.admin_crud_operations.service import service_crud
from src.filters.chat_types import LazyText as __

from src.database.crud.admin_crud_operations.category import category_crud
from src.keyboards.inline_kb import get_pagination_keyboard
from src.states.admin_state import AdminState


setup_logging()
logger = logging.getLogger(__name__)

admin_service_router = Router()


@admin_service_router.message(
    StateFilter(None),
    or_f(Command("create_service"),
         __("Создать услугу")))
async def before_create_service(
        message: types.Message,
        session: AsyncSession,
        state: FSMContext):

    categories = await category_crud.pagination(
        session=session,
        limit=10,
        skip=0)

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
        text.format(
            total_pages=total_pages),
        reply_markup=get_pagination_keyboard(
            total_pages=total_pages,
            current_page=1),
    )

    await state.set_state(AdminState.add_service)

@admin_service_router.message(
    StateFilter(AdminState.add_service),
    F.text)
async def create_service(
        message: types.Message,
        session: AsyncSession,
        state: FSMContext):

    try:

        (service_name,
         service_description,
         service_price,
         category_id_str) = message.text.split(" | ")

        service_name_cleaned = service_name.strip()
        service_description_cleaned = service_description.strip()
        category_id_cleaned = int(category_id_str.strip())
        service_price_cleaned = int(service_price.strip())


        if not await service_crud.exists(
                session=session,
                name=service_name_cleaned,
                category_id=category_id_cleaned):

            await service_crud.create(
                session=session,
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