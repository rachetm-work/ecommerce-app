import traceback

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.framework.exceptions import ServerError
from app.framework.exceptions import BaseCustomException
from app.framework.responses import ApiErrorResponse


class ExceptionMiddleware(BaseHTTPMiddleware):
    """
    This middleware will catch any exception that is raised from anywhere in the app and send an appropriate formatted response
    """

    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
        except Exception as e:
            return self.process_exception(e)

        return response

    @staticmethod
    def process_exception(exc):
        if isinstance(exc, BaseCustomException):
            error = exc
        else:
            error = ServerError(str(exc))

        traceback.print_exc()

        return ApiErrorResponse(error_message=error.error_message, error_code=error.status)
