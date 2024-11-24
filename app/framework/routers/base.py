from fastapi import APIRouter

from app.framework.settings import get_settings

settings = get_settings()

base_router = APIRouter(prefix=settings.BASE_URL_PREFIX)
