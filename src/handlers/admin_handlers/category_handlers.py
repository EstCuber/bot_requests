import math

from aiogram import Router, types, F
import logging
from src.core.logger import setup_logging
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.utils.i18n import I18n, gettext as _
from src.filters.chat_types import LazyText as __

from src.database.crud.admin_crud_operations.category import category_crud
from src.keyboards.inline_kb import get_pagination_keyboard
from src.states.admin_state import AdminState

setup_logging()
logger = logging.getLogger(__name__)

admin_category_router = Router()

@admin_category_router.message(StateFilter(None), or_f(Command("create_category"), __("Создать категорию")))
async def before_create_category(message: types.Message, state: FSMContext):

    await message.answer(_("Пожалуйста, введите категорию в формате:\n"
                   "Название категории | Описание категории"))
    await state.set_state(AdminState.add_category)

@admin_category_router.message(StateFilter(AdminState.add_category), F.text)
async def create_category(message: types.Message, session: AsyncSession, state: FSMContext):

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

@admin_category_router.callback_query(StateFilter(AdminState.add_service), F.data.startswith("category_page_"))
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