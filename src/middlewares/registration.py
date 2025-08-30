from locales.engine import i18n
from src.database.core.engine import session_maker
from .outer_middlewares import DataBaseSession, LanguageMiddleware, FSMI18nMiddleware


def register_middlewares(dp):
    dp.update.middleware.register(DataBaseSession(session_pool=session_maker)) # создает сессии
    dp.update.middleware.register(LanguageMiddleware(session_pool=session_maker)) # ловит язык пользователя с сессии
    dp.update.middleware.register(FSMI18nMiddleware(i18n)) # отвечает за i18n (интернационализация)