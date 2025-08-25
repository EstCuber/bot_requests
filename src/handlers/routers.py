from aiogram import Router
from .admin_handlers import *
from .user_handlers import *
from ..filters.chat_types import IsAdmin

admin_router = Router()
admin_router.message.filter(IsAdmin())

admin_router.include_routers(
    admin_start_router,
    admin_category_router,
    admin_service_router,
    work_with_admins_router,
    work_with_users_router
)

def include_admin_routers(dp):
    dp.include_routers(
        admin_router
    )

user_router = Router()
user_router.message.filter(~IsAdmin())

user_router.include_routers(
    start_user_router,
    main_menu_router
)

def include_user_routers(dp):
    dp.include_routers(
        user_router
    )