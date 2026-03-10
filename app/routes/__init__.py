from app.routes.auth import router as auth_router
from app.routes.users import router as users_router
from app.routes.products import router as products_router
from app.routes.orders import router as orders_router
from app.routes.suppliers import router as suppliers_router
from app.routes.dashboard import router as dashboard_router
from app.routes.contact import router as contact_router
from app.routes.inventory import router as inventory_router

__all__ = [
    "auth_router",
    "users_router",
    "products_router",
    "orders_router",
    "suppliers_router",
    "dashboard_router",
    "contact_router",
    "inventory_router",
]
