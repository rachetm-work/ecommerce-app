from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.framework.schemas import SuccessResponse, ErrorResponse


class ApiSuccessResponse(JSONResponse):
    def __init__(self, success=True, data=None, **kwargs):
        super().__init__(content=jsonable_encoder(SuccessResponse(success=success, data=data)), **kwargs)


class ApiErrorResponse(JSONResponse):
    def __init__(self, error_message, error_code='', **kwargs):
        errors = [{
            'error_message': error_message,
            'error_code': error_code
        }]
        super().__init__(content=jsonable_encoder(ErrorResponse(success=False, errors=errors)),
                         **kwargs)
