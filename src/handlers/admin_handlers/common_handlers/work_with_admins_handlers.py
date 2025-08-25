import logging

from aiogram import Router, types, F

from src.core.exceptions import ErrorCreateAdmin
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.utils.i18n import I18n, gettext as _

from src.core.logger import setup_logging
from src.core.settings import settings

setup_logging()
logger = logging.getLogger(__name__)


from src.database.crud.admin_crud_operations.common import create_admin, get_admins_list
from src.states.admin_state import AdminState

work_with_admins_router = Router()

@work_with_admins_router.message(StateFilter(None), Command("create_admin"))
async def start_create_admin(message: types.Message, state: FSMContext) -> None:
    await message.answer(_("Здравствуй, самый главный админ на районе. Пожалуйста, введи айди того глупца, который станет твоей новой звездой!"))
    await state.set_state(AdminState.add_admin)

@work_with_admins_router.message(StateFilter(AdminState.add_admin), F.text, F.message.from_user.id == settings.ADMIN_ID)
async def create_new_admin(message: types.Message, session: AsyncSession, state: FSMContext) -> None:
    telegram_id = int(message.text.strip())
    try:
        await create_admin(session=session, telegram_id=telegram_id)
        await message.answer(_("Админ успешно создан!"))
    except ErrorCreateAdmin as e:
        await message.answer(_("Не удалось создать админа, ошибка {}").format(e))
        logger.info(f"Не удалось создать админа, ошибка {e}")

    #TODO: просмотреть еще раз созданный crud, а также дополнительно обдумать логику с добавлением админов
    # Возможно, стоит добавить пагинацию для просмотра списка админов, а также проработать логику о том, что данная команда доступна только главному админу
