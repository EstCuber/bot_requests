

from aiogram.filters import Filter
from aiogram import types
from aiogram.utils.i18n import I18n

class ChatTypeFilter(Filter):
    """Фильтр для проверки типа чата:
    private, group, supergroup, channel < доступные типы"""
    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types

    async def __call__(self, message: types.Message) -> bool:
        return message.chat.type in self.chat_types

class IsAdmin(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message) -> bool:
        """
        TODO: продумать логику с админом, пока варианта три:
        1. Создать словарь в main, подключив его к bot. (Вариант рабочий конечно, но не подойдет, ибо админов каждый раз придется заново назначать)
        2. Использовать БД. Минус - создаст нагрузку на бд
        3. Возможно, Redis? Но придется тогда почитать о том, что это такое
        """

class LazyText(Filter):
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