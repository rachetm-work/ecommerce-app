from fastapi import APIRouter

from src.framework.settings import get_settings
from src.orders.routers import orders_router
from src.products.routers import products_router

settings = get_settings()

base_router = APIRouter(prefix=settings.BASE_URL_PREFIX)

base_router.include_router(products_router)
base_router.include_router(orders_router)
