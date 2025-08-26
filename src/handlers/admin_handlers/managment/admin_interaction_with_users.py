from aiogram import Bot, Router, types, F
import logging

from src.core.exceptions import ErrorSendAnswer
from src.core.logger import setup_logging
from aiogram.utils.i18n import I18n, gettext as _
from src.filters.chat_types import LazyText as __

setup_logging()
logger = logging.getLogger(__name__)

interaction_with_user_router = Router()

@interaction_with_user_router.message(
    F.reply_to_message,
    F.reply_to_message.forward_from
)
async def answer_to_user_message(
        message: types.Message,
        bot: Bot
) -> None:

    user_id = message.reply_to_message.forward_from.id

    admin_responce = message.text
    admin_name = message.from_user.full_name

    try:
        await bot.send_message(user_id, f"Вами получен ответ от:\n{admin_name}\n\n{admin_responce}")
        await message.answer(_("Ваш ответ был отправлен!"))
    except ErrorSendAnswer as e:
        await message.answer(_("Ошибка отправки сообщения! Ошибка: {}").format(e))
        logger.info(f"Ошибка отправки сообщения в админском хендлере, ошибка: {e}")