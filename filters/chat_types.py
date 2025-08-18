from aiogram.filters import Filter
from aiogram import types

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