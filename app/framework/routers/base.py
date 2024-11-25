from fastapi import APIRouter

from app.framework.settings import get_settings
from app.orders.routers import orders_router
from app.products.routers import products_router

settings = get_settings()

base_router = APIRouter(prefix=settings.BASE_URL_PREFIX)

base_router.include_router(products_router)
base_router.include_router(orders_router)
