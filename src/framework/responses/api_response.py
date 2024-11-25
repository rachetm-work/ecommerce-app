from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from src.framework.schemas import SuccessResponse, ErrorResponse
from src.framework.serializers import ApiModelSerializer


class ApiSuccessResponse(JSONResponse):
    def __init__(self, success=True, data=None, **kwargs):
        if isinstance(data, ApiModelSerializer):
            data = data.serialize()

        if not isinstance(data, list):
            data = [data]

        super().__init__(content=jsonable_encoder(SuccessResponse(success=success, data=data)), **kwargs)


class ApiErrorResponse(JSONResponse):
    def __init__(self, error_message, error_code=500, **kwargs):
        errors = [{
            'error_message': error_message,
            'error_code': error_code
        }]
        super().__init__(content=jsonable_encoder(ErrorResponse(success=False, errors=errors)),
                         status_code=error_code, **kwargs)
