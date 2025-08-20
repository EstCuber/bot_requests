from locales.engine import i18n
from src.database.core.engine import session_maker
from .outer_middlewares import DataBaseSession, LanguageMiddleware, FSMI18nMiddleware


def registration_middlewares(dp):
    dp.update.middleware.register(DataBaseSession(session_pool=session_maker))
    dp.update.middleware.register(LanguageMiddleware(session_pool=session_maker))
    dp.update.middleware.register(FSMI18nMiddleware(i18n))