from aiogram import Router
from .catalog import *
from .managment import info_router, user_iteraction_router
from .user_start import start_user_router
from src.filters.chat_types import IsAdmin

user_router = Router()
user_router.message.filter(~IsAdmin())
user_router.callback_query.filter(~IsAdmin())

user_router.include_routers(
    start_user_router,
    order_router,
    info_router,
    user_iteraction_router
)

def include_user_routers(dp):
    dp.include_routers(
        user_router
    )