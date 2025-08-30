from aiogram.filters.callback_data import CallbackData

class PageCallbackData(CallbackData, prefix="category_page_"):
    current_page: int

class CategoryPageCallbackData(CallbackData, prefix="category_page_"):
    current_page: int

class ServicePageCallbackData(CallbackData, prefix="service_"):
    category_id: int
    current_page: int