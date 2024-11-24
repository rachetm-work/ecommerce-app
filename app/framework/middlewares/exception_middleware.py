import traceback

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.framework.responses import ApiErrorResponse


class ExceptionMiddleware(BaseHTTPMiddleware):
    """
    This middleware will catch any exception that is raised from anywhere in the app and send an appropriate formatted response
    """

    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            traceback.print_exc()
            return ApiErrorResponse(error_message=str(e), status_code=500)
