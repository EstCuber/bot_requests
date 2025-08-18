
from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def create_kb(*btns: str,
              placeholder: str = None,
              request_contact: int = None,
              request_location: int = None,
              sizes: tuple[int] = (2,)) -> types.ReplyKeyboardMarkup:

    '''
    Параметры：
        request_contand, request_location = должны быть индексом той кнопки,
        для которой нужно подключить данные параметры
        Например:
        get_keyboard(
                "Меню",
                "О магазине",
                "Варианты оплаты",
                "Варианты доставки",
                "Отправить номер телефона"
                placeholder="Что вас интересует?",
                request_contact=4,
                sizes=(2, 2, 1)
            )
    '''

    keyboard = ReplyKeyboardBuilder()

    for index, text in enumerate(btns, start=0):

        if request_contact and request_contact == index:
            keyboard.button(text=text, request_contact=True)

        elif request_location and request_location == index:
            keyboard.button(text=text, request_location=True)

        else:
            keyboard.button(text=text)

    return keyboard.adjust(*sizes).as_markup(
        resize_keyboard=True,
        input_field_placeholder=placeholder
    )
