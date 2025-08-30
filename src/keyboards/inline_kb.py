from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.callback_data.user import PageCallbackData, ServicePageCallbackData


def get_callback_btns(*,
                      btns: dict[str, str],
                      sizes: tuple[int] = (2,),):
    keyboard = InlineKeyboardBuilder()

    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))
    return keyboard.adjust(*sizes).as_markup()


def get_url_btns(*,
                      btns: dict[str, str],
                      sizes: tuple[int] = (2,), ):
    keyboard = InlineKeyboardBuilder()

    for text, url in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, url=url))
    return keyboard.adjust(*sizes).as_markup()


def get_pagination_keyboard(*,
                            total_pages: int,
                            current_page: int = 1):
    builder = InlineKeyboardBuilder()

    if current_page > 1:
        builder.button(
            text="⬅️ Назад",
            callback_data=PageCallbackData(current_page=current_page - 1).pack()
        )

    if current_page < total_pages:
        builder.button(
            text="Вперед ➡️",
            callback_data=PageCallbackData(current_page=current_page + 1).pack()
        )

    builder.adjust(2)
    return builder.as_markup()

def service_pagination_kb(*,
                            total_pages: int,
                            current_page: int = 1,
                          category_id: int):
    builder = InlineKeyboardBuilder()

    if current_page > 1:
        builder.button(
            text="⬅️ Назад",
            callback_data=ServicePageCallbackData(current_page=current_page - 1, category_id=category_id).pack()
        )

    if current_page < total_pages:
        builder.button(
            text="Вперед ➡️",
            callback_data=ServicePageCallbackData(current_page=current_page + 1, category_id=category_id).pack()
        )

    builder.adjust(2)
    return builder.as_markup()