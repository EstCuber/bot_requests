from aiogram.utils.i18n import FSMI18nMiddleware
from locales.engine import i18n
from src.database.core.engine import session_maker
from src.middlewares.outer_middlewares.db_session import DataBaseSession
from src.middlewares.outer_middlewares.language_middleware import LanguageMiddleware


def registration_middlewares(dp):
    dp.update.middleware.register(DataBaseSession(session_pool=session_maker))
    dp.update.middleware.register(LanguageMiddleware(session_pool=session_maker))
    dp.update.middleware.register(FSMI18nMiddleware(i18n))