from aiogram import Router
from .catalog import *
from .managment import *
from .admin_start import admin_start_router
from src.filters.chat_types import IsAdmin

admin_router = Router()
admin_router.message.filter(IsAdmin())

admin_router.include_routers(
    admin_start_router,
    admin_category_router,
    admin_service_router,
    admin_interaction_router,
    interaction_with_user_router

)

def include_admin_routers(dp):
    dp.include_routers(
        admin_router
    )