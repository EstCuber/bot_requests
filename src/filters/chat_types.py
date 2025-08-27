

from aiogram.filters import Filter
from aiogram import types
from aiogram.utils.i18n import I18n

from src.core.settings import settings
from src.database.models.models import User, UserRole


class ChatTypeFilter(Filter):
    """
    Фильтр для проверки типа чата:
    private, group, supergroup, channel < доступные типы
    """
    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types

    async def __call__(self, message: types.Message) -> bool:
        return message.chat.type in self.chat_types

class IsAdmin(Filter):
    """
    фильтр, который проверяет главного админа (достает из settings),
    ИЛИ проверяет роль юзера из дб на то - является ли он админом
    DataBaseSession -> IsAdmin. Данная последовательность важна, потому что именно данный outer middleware дает ему db_user
    """
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, db_user: User | None) -> bool:
        if message.from_user.id == settings.ADMIN_ID:
            return True
        elif not db_user:
            return False

        return db_user.role == UserRole.admin


class LazyText(Filter):
    """
    Небольшой костыль, созданный для lazytext в i18n.
    Переводит под язык пользователя handlers с командами, пример:

    @<some_router>.message(or_f(Command(/exit), __("Выход")))
    async def __<function>(<parameters>):
        <your_code>

    Данный компонент необходим для работы кода, иначе я не смог придумать как сделать так, чтобы не поднималась ошибка,
    обычный lazy_text у меня не работает или я не понимаю как он должен работать
    """
    def __init__(self, text: str, ignore_case: bool = True) -> None:
        self.text = text
        self.ignore_case = ignore_case

    async def __call__(self, message: types.Message, i18n: I18n, locale: str) -> bool:
        if not message.text:
            return False

        translated = i18n.gettext(self.text, locale=locale)
        message_text = message.text

        if self.ignore_case:
            return message_text.lower() == translated.lower()

        return message_text == translated