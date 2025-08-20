from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

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
            callback_data=f"category_page_{current_page - 1}"
        )

    if current_page < total_pages:
        builder.button(
            text="Вперед ➡️",
            callback_data=f"category_page_{current_page + 1}"
        )

    builder.adjust(2)
    return builder.as_markup()