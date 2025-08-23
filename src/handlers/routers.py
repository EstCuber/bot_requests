from .admin_handlers import *

def include_admin_routers(dp):
    dp.include_routers(admin_start_router,
                       admin_category_router,
                       admin_service_router)